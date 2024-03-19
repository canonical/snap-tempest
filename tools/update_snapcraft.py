"""Update the snapcraft yaml file.

This module implements a command line application that parses the latest
tempest, tempest plugins and python-tempestconf release information from
the OpenStack releases repository and the PYPI RSS feed and modifies the
snapcraft.yaml file inplace to reflect the changes, should there be any.
"""

import io
import logging
import shutil
import sys
import tempfile
from argparse import ArgumentParser
from functools import cmp_to_key
from pathlib import Path

import feedparser
import pygit2
from packaging import version
from packaging.requirements import InvalidRequirement, Requirement
from ruamel.yaml import YAML

logger = logging.getLogger(__name__)
yaml = YAML(typ="rt")

RELEASES_REPO_URL = "https://opendev.org/openstack/releases.git"
RELEASES_REPO_PATH = Path(tempfile.gettempdir()) / "releases"
OPENDEV_BASE_URL = "git+https://opendev.org"
OPENSTACK_REPO_URL_FMT = OPENDEV_BASE_URL + "/openstack/{project}.git@{ref}"
OPENINFRA_REPO_URL_FMT = OPENDEV_BASE_URL + "/openinfra/{project}.git@{ref}"
PYPI_RSS_FEED_FMT = "https://pypi.org/rss/project/{project}/releases.xml"
MANUAL_REQUIREMENTS = Path(__file__).parents[1] / Path("requirements-manual.txt")


def parse_manual_requirements(path):
    """Parse a requirements.txt path.

    Ingests a path and returns a set of requirement strings.
    Comments are stripped, and invalid requirements are skipped.
    """
    manual_requirements = set()

    if path.exists():
        with open(path, encoding="utf-8") as req_file:
            for line in req_file:
                try:
                    # Requirement cannot handle comments
                    req = Requirement(line.split("#", maxsplit=1)[0])
                    manual_requirements.add(str(req))
                except InvalidRequirement:
                    pass

    return manual_requirements


def parse_args():
    """Parse command line arguments."""
    parser = ArgumentParser()
    parser.add_argument("-r", "--release", required=True, type=str, help="OpenStack release")
    parser.add_argument(
        "-o", "--output", default="/dev/stdout", type=str, help="Output file. Defaults to stdout"
    )
    parser.add_argument(
        "--reuse",
        default=False,
        action="store_true",
        help=(
            "Reuse the existing releases repository. When this option is given, "
            "the script will not delete the clone releases repository upon exiting. "
            "This option is helpful for running this script locally in a sequential fashion."
        ),
    )
    return parser.parse_args()


def get_latest_revision_from_release_file(path):
    """Get the latest revision from yaml formatted release files."""
    content = yaml.safe_load(path.read_text())
    revisions = [release["version"] for release in content["releases"]]
    return (
        f"{path.parent.stem}-last"
        if f"{path.parent.stem}-last" in revisions
        else max(revisions, key=cmp_to_key(semver.compare))
    )


def get_latest_tempest_revision(release):
    """Return the requirements entry for the latest tempest revision."""
    return get_latest_revision_from_release_file(
        RELEASES_REPO_PATH / "deliverables" / release / "tempest.yaml"
    )


def get_latest_plugin_requirements(release):
    """Return list of requirements entries for the latest tempest plugin revisions."""
    result = []

    for file_path in (RELEASES_REPO_PATH / "deliverables" / release).iterdir():
        metadata = yaml.load(file_path.read_text())
        if metadata["type"] == "tempest-plugin":
            project = list(metadata["repository-settings"])[0]
            feed_url = OPENSTACK_TAGS_RSS_FEED_FMT.format(project=project)
            tag = get_latest_tag_from_feed(feed_url, release)
            result.append(OPENSTACK_REPO_URL_FMT.format(project=project, ref=tag))

    return sorted(result)


def get_latest_tempestconf_requirements():
    """Return the requirements entry for the latest python-tempestconf revision."""
    project = "python-tempestconf"
    latest_revision = feedparser.parse(PYPI_RSS_FEED_FMT.format(project=project)).entries[0].title
    return OPENINFRA_REPO_URL_FMT.format(project=project, ref=latest_revision)


def clone_releases_repository(reuse):
    """Clone the OpenStack releases repository.

    If the reuse flag is given, try to reuse the existing repository.
    """
    if not RELEASES_REPO_PATH.exists():
        logger.info("Cloning releases repository")
        pygit2.clone_repository(RELEASES_REPO_URL, RELEASES_REPO_PATH)
    elif reuse:
        repo_path = pygit2.discover_repository(RELEASES_REPO_PATH)
        if not repo_path:
            raise RuntimeError(
                f"Reuse flag given however {RELEASES_REPO_PATH} is not a git repository."
            )
        if pygit2.Repository(repo_path).remotes["origin"].url != RELEASES_REPO_URL:
            raise RuntimeError(
                f"Repository: {repo_path} does not list {RELEASES_REPO_URL} as origin."
            )
        logger.info("Using the repository at %s", repo_path)
    else:
        raise RuntimeError(f"Reuse flag not given and {RELEASES_REPO_PATH} exists.")


def main(args):
    """Entry point to the application."""
    clone_releases_repository(args.reuse)
    snapcraft_yaml_path = Path(__file__).parent.parent / "snap" / "snapcraft.yaml"
    snapcraft_yaml = yaml.load(snapcraft_yaml_path.read_text())

    # Don't go back to an earlier Tempest version if it has been manually overridden
    current_tempest_revision = snapcraft_yaml["parts"]["tempest"]["source-tag"]
    latest_tempest_revision = get_latest_tempest_revision(args.release)
    if version.parse(latest_tempest_revision) > version.parse(current_tempest_revision):
        snapcraft_yaml["parts"]["tempest"]["source-tag"] = latest_tempest_revision

    # Update plugin versions unconditionally
    snapcraft_yaml["parts"]["tempest"]["python-packages"] = [
        *parse_manual_requirements(MANUAL_REQUIREMENTS),
        *get_latest_plugin_requirements(args.release),
        get_latest_tempestconf_requirements(),
    ]

    output_str = io.StringIO()
    yaml.dump(snapcraft_yaml, output_str)
    Path(args.output).write_text(output_str.getvalue(), encoding="utf-8")
    if not args.reuse:
        shutil.rmtree(RELEASES_REPO_PATH)
    return 0


def str_presenter(dumper, data):
    """Configure yaml for dumping multiline strings."""
    if len(data.splitlines()) > 1:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
    yaml.default_flow_style = False
    yaml.Representer.add_representer(str, str_presenter)
    sys.exit(main(parse_args()))
