"""Load tempest's entry points with the snap's own interpreter.

cliff silently drops a tempest command whose module fails to import, so
`tempest --help` still succeeds and `tempest run` just reports an unknown
command. Loading the entry points directly surfaces the import error.
"""

import subprocess

LOAD_ENTRY_POINTS = """
import importlib.metadata
import sys

group, instantiate = sys.argv[1], sys.argv[2] == "1"
eps = importlib.metadata.entry_points()
# entry_points().select() needs Python >= 3.10; older bases return a dict
eps = list(eps.select(group=group) if hasattr(eps, "select") else eps.get(group, []))
if not eps:
    sys.exit(f"no entry points found in group {group!r}")
broken = {}
for ep in eps:
    try:
        loaded = ep.load()
        if instantiate:
            loaded()
    except Exception as exc:
        broken[ep.name] = repr(exc)
if broken:
    sys.exit(f"failed to load from group {group!r}: {broken}")
"""


def load_entry_points(group, instantiate):
    """Load every entry point of a group inside the snap and return the process result."""
    return subprocess.run(
        ["snap", "run", "--shell", "tempest", "-c", f"python3 - {group} {int(instantiate)}"],
        input=LOAD_ENTRY_POINTS,
        capture_output=True,
        text=True,
    )


def test_tempest_commands_load():
    """Test every tempest CLI command imports."""
    result = load_entry_points("tempest.cm", instantiate=False)
    assert result.returncode == 0, result.stderr


def test_tempest_plugins_load():
    """Test every bundled tempest plugin imports and instantiates, as tempest run does."""
    result = load_entry_points("tempest.test_plugins", instantiate=True)
    assert result.returncode == 0, result.stderr
