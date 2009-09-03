import sys
sys.path.append(".")

from igor.vcs import NullVCS, get, project_type
from igor.vcs.git import Git


def test_vcs_type(project):
    pt = project_type(project)
    assert(pt == "git")

def test_get():
    assert(get("git") == Git)
    assert(get(None) == NullVCS)

