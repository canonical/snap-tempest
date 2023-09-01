"""Update the snapcraft yaml file.

This module implements a command line application that parses the latest
tempest, tempest plugins and python-tempestconf release information from
the OpenStack releases repository and the PYPI RSS feed and modifies the
snapcraft.yaml file inplace to reflect the changes, should there be any.
"""
import logging
import shutil
import sys
from argparse import ArgumentParser
from functools import cmp_to_key
from pathlib import Path

import feedparser
import pygit2
import semver
import yaml

logger = logging.getLogger(__name__)

RELEASES_REPO_URL = "https://opendev.org/openstack/releases.git"
RELEASES_REPO_PATH = Path("~/.local/share/snap-tempest/releases").expanduser()
OPENDEV_BASE_URL = "git+https://opendev.org"
OPENSTACK_REPO_URL_FMT = OPENDEV_BASE_URL + "/openstack/{project}.git@{ref}"
OPENINFRA_REPO_URL_FMT = OPENDEV_BASE_URL + "/openinfra/{project}.git@{ref}"
PYPI_RSS_FEED_FMT = "https://pypi.org/rss/project/{project}/releases.xml"


def parse_args():
    """Parse command line arguments."""
    parser = ArgumentParser()
    parser.add_argument("-r", "--release", required=True, type=str, help="OpenStack release")
    parser.add_argument(
        "-o", "--output", default="/dev/stdout", type=str, help="Output file. Defaults to stdout"
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
    plugin_release_file_paths = [
        entry
        for entry in (RELEASES_REPO_PATH / "deliverables" / release).iterdir()
        if entry.is_file() and yaml.safe_load(entry.read_text())["type"] == "tempest-plugin"
    ]
    for path in plugin_release_file_paths:
        try:
            latest_revision = get_latest_revision_from_release_file(path)
            result.append(OPENSTACK_REPO_URL_FMT.format(project=path.stem, ref=latest_revision))
        except KeyError as exception:
            logger.warning("Skipping path:[%s], error:[%s]", path, repr(exception))
    return sorted(result)


def get_latest_tempestconf_requirements():
    """Return the requirements entry for the latest python-tempestconf revision."""
    project = "python-tempestconf"
    latest_revision = feedparser.parse(PYPI_RSS_FEED_FMT.format(project=project)).entries[0].title
    return OPENINFRA_REPO_URL_FMT.format(project=project, ref=latest_revision)


def clone_releases_repository():
    """Clone the OpenStack releases repository.

    If the repository exists, just fetch origin and fast-forward
    to the tip of the current remote default branch.

    If fast forwarding is not possible, e.g. repo is dirty,
    remove the repo and reclone.
    """
    RELEASES_REPO_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        pygit2.clone_repository(RELEASES_REPO_URL, RELEASES_REPO_PATH)
    except ValueError as error:
        repo_path = pygit2.discover_repository(RELEASES_REPO_PATH)
        if not repo_path:
            raise RuntimeError(
                f"{RELEASES_REPO_PATH} is not empty and not a git repository"
            ) from error

        repo = pygit2.Repository(repo_path)
        repo.checkout("refs/heads/master")
        repo.remotes["origin"].fetch()
        remote_master_id = repo.lookup_reference("refs/remotes/origin/master").target
        analysis_result, _ = repo.merge_analysis(remote_master_id)

        if analysis_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
            logger.info("Release repository up to date")
            return

        if analysis_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
            # pygit2 does not expose a simple way to perform a ff merge
            # the following is a manual ff merge:
            # checkout to the remote master reference object
            # then update the local master to match it
            logger.info("Updating release repository")
            repo.checkout_tree(repo.get(remote_master_id))
            try:
                master_ref = repo.lookup_reference("refs/heads/master")
                master_ref.set_target(remote_master_id)
            except KeyError:
                repo.create_branch("master", repo.get(remote_master_id))
            repo.head.set_target(remote_master_id)
        else:
            # ff merge not available. We might as well reclone. it will be messy otherwise
            logger.info("Release repository not clean. Recloning.")
            shutil.rmtree(RELEASES_REPO_PATH)
            pygit2.clone_repository(RELEASES_REPO_URL, RELEASES_REPO_PATH)


def main(args):
    """Entry point to the application."""
    clone_releases_repository()
    snapcraft_yaml_path = Path(__file__).parent.parent / "snap" / "snapcraft.yaml"
    snapcraft_yaml = yaml.safe_load(snapcraft_yaml_path.read_text())

    snapcraft_yaml["parts"]["tempest"]["source-tag"] = get_latest_tempest_revision(args.release)
    snapcraft_yaml["parts"]["tempest"]["python-packages"] = [
        "confluent-kafka==1.8.2",
        *get_latest_plugin_requirements(args.release),
        get_latest_tempestconf_requirements(),
    ]

    Path(args.output).write_text(yaml.safe_dump(snapcraft_yaml, sort_keys=False), encoding="utf-8")
    return 0


def str_presenter(dumper, data):
    """Configure yaml for dumping multiline strings."""
    if len(data.splitlines()) > 1:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
    yaml.representer.SafeRepresenter.add_representer(str, str_presenter)
    sys.exit(main(parse_args()))
