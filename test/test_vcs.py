import sys
import os
sys.path.append(".")

from igor.vcs import type, get, NullVCS
from igor.vcs.git import Git

test_project = "./igor_extras/initial_project"

def test_vcs_type():
    assert(type(test_project), "none")

def test_get():
    assert(get("git") == Git)
    assert(get("none") == NullVCS)

    
