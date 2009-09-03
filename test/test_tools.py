import sys
from os import path, listdir
from shutil import rmtree

sys.path.append(".")

from igor.tools import find_files, make_posts, publish, init
from igor.documents import Document

def test_find_files(project):
    posts_path = path.join(project, "_posts")
    extensions = [".txt", ".mkd"]
    files = list(find_files(posts_path, extensions=extensions))
    assert(len(files) >= 1)

    for file in files:
        name, ext = path.splitext(file)
        assert(path.exists(file))
        assert(ext in extensions)

def test_make_posts(project):
    ps = list(make_posts(project,
              "_posts",
              extensions = [".txt", ".mkd"]))
    assert(len(ps) >= 1)

def test_publish(project):
    destination = "/tmp/blog.test"
    published = publish(project, destination)
    assert(published)
    assert(path.exists("/tmp/blog.test"))
    assert(path.exists("/tmp/blog.test/index.html"))
    assert(path.exists("/tmp/blog.test/feed.atom"))
    rmtree(destination)
    # It would be great to add a test for the existance of a post

def test_init():
    destination = "/tmp/igor.test"
    try:
        rmtree(destination)
    except:
        pass

    init(destination)
    assert(path.exists(destination))
    assert(path.exists(path.join(destination, "_posts")))
    assert(path.exists(path.join(destination, "_templates")))
    assert(path.exists(path.join(destination, "media")))
    assert(path.exists(path.join(destination, "_config.yaml")))
    rmtree(destination)
