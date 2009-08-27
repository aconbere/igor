import sys
import os

sys.path.append(".")

from igor.publisher import Publisher

test_dest = ""
test_template_dir = ""
test_context = {} 

def test_publisher():
    p = Publisher(test_dest, test_template_dir, test_context)
    post = Post()
    p.publish(p)
    assert(False):
