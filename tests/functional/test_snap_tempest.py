import subprocess


def test_tempest_help_string():
    """Test tempest prints the help string."""
    assert 0 == subprocess.run(["tempest", "--help"]).returncode


def test_tempestconf_help():
    """Test python-tempestconf prints the help."""
    assert 0 == subprocess.run(["tempest.discover", "--help"]).returncode
    # TODO: remove this after auto-aliasing is enabled
    assert (
        0
        == subprocess.run(
            ["sudo", "snap", "alias", "tempest.discover", "discover-tempest-config"]
        ).returncode
    )
    assert 0 == subprocess.run(["discover-tempest-config", "--help"]).returncode
