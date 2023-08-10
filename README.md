# Tempest Snap

This repository contains the source code of the snap for the OpenStack integration
test suite, Tempest.

## Installing this snap

The tempest snap can be installed directly from the snap store:

    sudo snap install --edge tempest


## Plugins

The image is baked with all plugins listed in the release notes and those cannot be
removed or updated. Currently, it is not possible to add new plugins or use your own.

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
