import sys
import os
sys.path.append(".")

from igor.blog_parser import FileParser


def test_initialize_file_parser():
    fp = FileParser("examples/basic/", "_posts/example.txt")
    assert(fp)
    return fp

def test_pop_section():
    sections = ["this is the first section", "this is the second"]
    test_string = "\n\n".join(sections)

    with open("/tmp/test_string.txt", 'w') as f:
        f.write(test_string)

    with open("/tmp/test_string.txt", 'r') as f:
        fp = test_initialize_file_parser()
        section = fp._pop_section(f)
        assert(section == sections[0])
        assert(f.read() == sections[1])
