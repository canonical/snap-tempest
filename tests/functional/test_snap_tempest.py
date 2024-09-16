import subprocess


def test_tempest_help_string():
    """Test tempest prints the help string."""
    output = subprocess.check_output(["tempest", "--help"])
    assert b"usage: tempest" in output


def test_tempestconf_help():
    """Test python-tempestconf prints the help."""
    output = subprocess.check_call(["tempest.discover", "--help"])
    assert b"usage:" in output
