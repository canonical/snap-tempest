# Tempest Snap

This repository contains the source code of the snap for the OpenStack integration
test suite, Tempest.

Alongside with the tempest project, this snap also includes the currently maintained tempest plugins,
the [python-tempestconf] package and several curated test lists to provide ease of use.

The [python-tempestconf] package provides [`discover-tempest-config`] command line
application that automatically generates a tempest configuration appropriate for your cloud.

## Installing this snap

The tempest snap can be installed directly from the snap store:

    sudo snap install [INSTALL-OPTIONS] tempest

## Compatibility matrix

With version numbers not being aligned between Tempest, the various Tempest
plugins, and OpenStack releases, it is not immediately obvious which set of
components are compatible with each other.

The Tempest snap simplifies testing OpenStack clouds by providing
release-specific channels, which package all the correct Tempest and Tempest
plugin versions for the relative OpenStack release.

The default channel for this snap is the stable channel for the latest current
OpenStack release, e.g. `2023.1/stable` if Antelope is the most recent release.
To test older clouds, please specify an alternate channel. For example, in a
Yoga OpenStack cloud, users can install the Tempest snap from the `yoga/stable`
channel:

    sudo snap install --channel yoga/stable tempest

Further details about the compatibility of the various components are available
in the upstream documentation:
- [OpenStack Antelope release notes - Tempest plugins]
- [Tempest release notes]

## Plugins

The snap provides all the plugins listed in the [OpenStack release notes] and those
cannot be removed or updated. Currently, it is not possible to add new plugins or use
your own.

List of plugins:

- barbican-tempest-plugin
- blazar-tempest-plugin
- cinder-tempest-plugin
- cloudkitty-tempest-plugin
- cyborg-tempest-plugin
- designate-tempest-plugin
- ec2api-tempest-plugin
- freezer-tempest-plugin
- glance-tempest-plugin
- heat-tempest-plugin
- ironic-tempest-plugin
- keystone-tempest-plugin
- kuryr-tempest-plugin
- magnum-tempest-plugin
- manila-tempest-plugin
- mistral-tempest-tests
- monasca-tempest-plugin
- murano-tempest-plugin
- neutron-tempest-plugin
- octavia-tempest-plugin
- oswin-tempest-plugin
- sahara-tests
- senlin-tempest-plugin
- solum-tempest-plugin
- telemetry-tempest-plugin
- trove-tempest-plugin
- venus-tempest-plugin
- vitrage-tempest-plugin
- watcher-tempest-plugin
- zaqar-tempest-plugin
- zun-tempest-plugin


## Quickstart
Running the tempest smoke suite against a deployed OpenStack cloud would look like this.

```
# Install the tempest snap from the latest/edge channel
sudo snap install tempest --edge

# Have the cloud credentials in the environment
source novarc

# Initialize a tempest workspace directory called cloud-01
tempest init cloud-01 && cd cloud-01

# Generate the tempest configuration specific to the cloud
discover-tempest-config

# Run the tempest smoke suite
tempest run --smoke
```
For more information please refer to the [Tempest QuickStart] and [python-tempestconf] documentation.

## Test Lists
The tempest snap bundles a set of pre-defined test lists.
They can be found at `/snap/tempest/current/lists/`.

```
$ ls /snap/tempest/current/lists/
readonly-quick  refstack-2022.11

$ tempest run --load-list /snap/tempest/current/lists/readonly-quick
```

### readonly-quick
For quickly verifying the behavior of the target cloud and making sure tempest
is correctly set up.

```
tempest run --load-list /snap/tempest/current/lists/readonly-quick
```

### refstack-2022.11
Version 2022.11 of the [RefStack] guidelines.
The list includes the required and advisory tests of all platforms.

```
tempest run --load-list /snap/tempest/current/lists/refstack-2022.11
```

[OpenStack Antelope release notes - Tempest plugins]: https://releases.openstack.org/antelope/index.html#tempest-plugins
[Tempest release notes]: https://docs.openstack.org/releasenotes/tempest/unreleased.html
[python-tempestconf]: https://opendev.org/openinfra/python-tempestconf
[`discover-tempest-config`]: https://docs.opendev.org/openinfra/python-tempestconf/latest/cli/cli_options.html#discover-tempest-config
[Tempest QuickStart]: https://docs.openstack.org/tempest/latest/overview.html#quickstart
[RefStack]: (https://refstack.openstack.org/#/)
