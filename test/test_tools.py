import sys
from os import path, listdir

sys.path.append(".")

from igor.tools import find_files, make_posts, publish
from igor.documents import Document

def test_find_files():
    extensions = [".txt", ".mkd"]
    files = list(find_files(path.abspath("./examples/init/_posts"), extensions=extensions))
    assert(len(files) >= 1)
    for file in files:
        name, ext = path.splitext(file)
        assert(path.exists(file))
        assert(ext in extensions)

def test_make_posts():
    ps = list(make_posts("./examples/init/",
              "_posts",
              extensions = [".txt", ".mkd"]))
    assert(len(ps) >= 1)

def test_publish():
    from shutil import rmtree
    rmtree("/tmp/igor.test")
    Document.clear()
    published = publish("./examples/init", "/tmp/igor.test")
    assert(published)
    assert(path.exists("/tmp/igor.test"))
    assert(path.exists("/tmp/igor.test/index.html"))
    assert(path.exists("/tmp/igor.test/feed.atom"))
    # It would be great to add a test for the existance of a post
