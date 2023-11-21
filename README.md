# Tempest Snap

This repository contains the source code of the snap for the OpenStack integration
test suite, Tempest.

Alongside with the tempest project, this snap also includes the currently maintained tempest plugins,
the [python-tempestconf] package and several curated test lists to provide ease of use.

The [python-tempestconf] package provides [`discover-tempest-config`] command line
application that automatically generates a tempest configuration appropriate for your cloud.

## Installing this snap

The tempest snap can be installed directly from the snap store:

    sudo snap install [install-OPTIONS] tempest

By default, tempest snap will be installed from the stable channel of the latest OpenStack
release, e.g. `2023.1/stable` if `antelope` is the most recent release, unless a different
channel is explicitly specified. This channel is generally compatible with actively developed
OpenStack releases thanks to the relatively flexible alignment between Tempest and its plugins
with OpenStack versions. 

For a more tailored installation, users have the option to choose the channel that is designed
for their cloud environment. For example, in a `yoga` OpenStack cloud, users can install tempest
snap from the `yoga/stable` channel:

    sudo snap install --channel yoga/stable tempest

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
The tempest snap provides a set of pre-defined test lists with different profiles
and a mechanism to specify them easily.

The `@BUILTIN_TESTLISTS` keyword will be automatically replaced by the full path
of the directory storing the built-in test lists.

**Note**: the single-quotation marks around the test list file path is required
if the `@BUILTIN_TESTLISTS` keyword is used (in other words, when running tempest
with a built-in test list file). Failure to do so will result in a wrong path
error.

### readonly-quick
For quickly verifying the behavior of the target cloud and making sure tempest
is correctly set up

    tempest run --load-list '@BUILTIN_TESTLISTS/readonly-quick'

### refstack-2022.11
Version 2022.11 of the [RefStack] guidelines.
The list includes the required and advisory tests of all platforms.

    tempest run --load-list '@BUILTIN_TESTLISTS/refstack-2022.11'

[OpenStack release notes]: https://releases.openstack.org/antelope/index.html#tempest-plugins
[python-tempestconf]: https://opendev.org/openinfra/python-tempestconf
[`discover-tempest-config`]: https://docs.opendev.org/openinfra/python-tempestconf/latest/cli/cli_options.html#discover-tempest-config
[Tempest QuickStart]: https://docs.openstack.org/tempest/latest/overview.html#quickstart
[RefStack]: (https://refstack.openstack.org/#/)
