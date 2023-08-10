import subprocess


def test_tempest_help_string():
    """Test tempest prints the help string."""
    assert 0 == subprocess.run(["tempest", "--help"]).returncode
