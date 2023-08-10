import os
import subprocess

import pytest


@pytest.fixture(scope="session", autouse=True)
def install_tempest_snap():
    snap = os.environ["TEST_SNAP"]
    process = subprocess.run(["sudo", "snap", "install", "--dangerous", snap])
    assert 0 == process.returncode
    yield
    subprocess.run(["sudo", "snap", "remove", "--purge", "tempest"])
