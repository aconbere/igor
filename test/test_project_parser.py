import sys
import os

sys.path.append(".")

from igor.project_parser import ProjectParser
from igor.documents import Post

def test_intialize():
    p = ProjectParser("./examples/basic", "/tmp/igor_tests")
    assert(p)

def test_organize_posts():
    p1 = Post("./examples/basic/_posts/example.txt", "./examples/basic")
    p2 = Post("./examples/basic/_posts/markdown_post.mkd", "./examples/basic")
    p3 = Post("./examples/basic/_posts/subdir/info.txt", "./examples/basic")

    p = ProjectParser("./examples/basic", "/tmp/igor_tests")
    org = p.organize_posts_by_date([p1,p2,p3])
    test_org = {2009: {1: {11 : [p1]},
                       7: {21: [p3],
                           22: [p2],}
                      }
               }

    
    assert(org == test_org)
