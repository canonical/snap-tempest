import subprocess

import pytest


@pytest.fixture(scope="session", autouse=True)
def install_tempest_snap():
    subprocess.check_call("sudo snap install --dangerous ./tempest_*.snap", shell=True)

    yield

    subprocess.run(["sudo", "snap", "remove", "--purge", "tempest"])
