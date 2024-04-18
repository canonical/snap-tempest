# Components update automation

This repository has to maintain a correct list of components and versions in `snapcraft.yaml`: Tempest itself, python-tempestconf, and the various Tempest plugins we want to bundle. This is particularly important because only specific sets of versions are compatible with each other.

Additionally, we need to ensure we update the bundled components as new releases are created upstream.

This process is managed via GitHub workflows stored in a separate repo, [snap-tempest-automation](https://github.com/canonical/snap-tempest/).

The workflows run periodically, but can also be triggered manually via the GitHub API.

For any supported OpenStack release, the workflows will generate PRs in this repository from a `release/<codename>` branch, targeting the corresponding `stable/<codename>` one, providing updated component versions. It is possible to affect the algorithm on a per-branch basis by providing two optional files at the root of this present repository:
* `excluded-plugins.txt`: this is a list of Tempest plugin names that should not be bundled in the snap. A default list is held within the  [snap-tempest-automation](https://github.com/canonical/snap-tempest/) repo.
* `requirements-manual.txt`: this is a list of additional Python packages that should be bundled in the snap, in PEP440 format. This may sometimes be required to fix missing plugin dependencies. By default, no additional requirements are installed.

As an example, committing an `excluded-plugins.txt` file at the root of the `stable/yoga` branch with the content "`keystone-tempest-plugin`" would cause the automation to propose a PR from `release/yoga` to `stable/yoga` to bundle all known Tempest plugins compatible with OpenStack Yoga, except for the Keystone one.

More details about these workflows are available in the [snap-tempest-automation](https://github.com/canonical/snap-tempest/) repo.