import subprocess


def test_tempest_help_string():
    """Test tempest prints the help string."""
    output = subprocess.check_output(["tempest", "--help"])
    assert b"usage: tempest" in output


def test_tempestconf_help():
    """Test python-tempestconf prints the help."""
    # aliases aren't created yet
    subprocess.check_call(["sudo", "snap", "alias", "tempest.discover", "discover-tempest-config"])
    output1 = subprocess.check_call(["tempest.discover", "--help"])
    output2 = subprocess.check_output(["discover-tempest-config", "--help"])
    assert output1 == output2
    assert b"usage:" in output2
