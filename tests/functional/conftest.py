import subprocess

import pytest


@pytest.fixture(scope="session", autouse=True)
def install_tempest_snap():
    # core26 is not yet in stable; pre-install from edge so that
    # --dangerous installs of core26-based snaps resolve their base.
    subprocess.run(["sudo", "snap", "install", "core26", "--channel=latest/edge"])
    subprocess.check_call("sudo snap install --dangerous ./tempest_*.snap", shell=True)

    yield

    subprocess.run(["sudo", "snap", "remove", "--purge", "tempest"])
