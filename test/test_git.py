import sys
import os
from os import path
sys.path.append(".")

from igor.vcs.git import Git

def test_git(project):
    file = path.join(project, "_posts/welcome.txt")
    g = Git(project, file)
    assert(g.author_email())
    assert(g.date())
    assert(g.author())
    assert(g.data())
