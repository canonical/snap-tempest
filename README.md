# Tempest Snap

This repository contains the source code of the snap for the OpenStack integration
test suite, Tempest.

## Installing this snap

The tempest snap can be installed directly from the snap store:

    sudo snap install --edge tempest


## This snap includes

### python-tempestconf

This snapshot includes [python-tempestconf](https://opendev.org/openinfra/python-tempestconf),
which automatically generates a tempest configuration based on your cloud.

It provided single CLI options [`discover-tempest-config`](https://docs.opendev.org/openinfra/python-tempestconf/latest/cli/cli_options.html#discover-tempest-config),
which is provided in snap via `tempest.discover`.