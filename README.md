# Tempest Snap

This repository contains the source code of the snap for the OpenStack integration
test suite, Tempest.

## Installing this snap

The tempest snap can be installed directly from the snap store:

    sudo snap install --edge tempest


## Quickstart
To run Tempest, please follow the steps in [Tempest QuickStart](https://docs.openstack.org/tempest/latest/overview.html#quickstart) documentation.

The tempest snap provides a set of pre-defined test lists with different focuses. For quickly verifying the behavior of the objective cloud and making sure tempest is correctly set up, you can run tests listed in the `readonly-quick.txt` file:

    tempest run --load-list '@BUILDIN_TESTLISTS/readonly-quick.txt' 

`@BUILDIN_TESTLISTS` keyword will be automatically replaced by the full path of the directory storing the built-in test lists.

**Note**: the single-quotation marks around the test list file path is required if `@BUILDIN_TESTLISTS` keyword is used (in another words, when running tempest with a built-in test list file). Fail to do that will result in wrong path error.


## This snap includes

### python-tempestconf

This snapshot includes [python-tempestconf](https://opendev.org/openinfra/python-tempestconf),
which automatically generates a tempest configuration based on your cloud.

It provided single CLI options [`discover-tempest-config`](https://docs.opendev.org/openinfra/python-tempestconf/latest/cli/cli_options.html#discover-tempest-config),
which is provided in snap via `tempest.discover`.
