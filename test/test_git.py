import sys
import os
sys.path.append(".")

from igor.vcs.git import Git

test_project = "./igor_extras/initial_project"
test_file = path.join(test_project, "_posts/welcome.txt")

def test_git():
    g = Git(test_project, test_file)
    assert(g.author_email())
    assert(g.published_date())
    assert(g.author())
    assert(g.data())
