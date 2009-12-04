import sys
import os
sys.path.append(".")

from igor.vcs.git.ls_tree import ListTree, ListElement

test_project = "/tmp/igor.test"

def test_list_item_parsing():
    test_element = ListElement("100644", "blob", "ddec4c671efebd5b61b219d2de49c828f6a4d956", "_gitignore")
    l = ListElement.from_string("100644 blob ddec4c671efebd5b61b219d2de49c828f6a4d956    _gitignore")
    assert(str(test_element) == str(l))

def test_list_parsing():
    test_list = """\
100644 blob 902edab1599d6bcb08854e004362a6af2889ffbb    _config.yaml
040000 tree 5798430982f287bb3de76f8c00dff666f2df8f14    _templates
100644 blob 33436dc95ca1755a459a4dd9f7992b45008f3837    example.txt
    """

    l = ListTree(test_project)
    elements = l.parse_list(test_list)
    assert_data = [
        ListElement("100644", "blob", "902edab1599d6bcb08854e004362a6af2889ffbb", "_config.yaml"),
        ListElement("040000", "tree", "5798430982f287bb3de76f8c00dff666f2df8f14", "_templates"),
        ListElement("100644", "blob", "33436dc95ca1755a459a4dd9f7992b45008f3837", "example.txt"),
        ]
    assert([str(s) for s in elements] == [str(s) for s in assert_data])

def test_list_retrieval(project):
    l = ListTree(project)
    l.call()
    assert(len(l.elements) > 0)
