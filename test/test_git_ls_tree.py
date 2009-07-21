import sys
import os
sys.path.append("..")
sys.path.append(".")

from git_wrapper.ls_tree import ListTree

def test_list_retrieval():
    os.chdir("test/example")
    l = ListTree()
    l.call()
    print(l.elements)
    assert(False)
    
