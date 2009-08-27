import sys
from os import path

sys.path.append(".")

from igor.tools import prepare_paths, find_files, find_posts, environment, config

def test_find_files():
    extensions = [".txt", ".mkd"]
    files = list(find_files(path.abspath("./examples/init/_posts"), extensions=extensions))
    assert(len(files) >= 1, "No files returned")
    for file in files:
        name, ext = path.splitext(file)
        assert(path.exists(file), "File does not exist")
        assert(ext in extensions, "File was not of type found in extensions filter")

def test_make_posts():
    ps = list(make_posts("./examples/init/",
              prefix="_posts",
              extensions = [".txt", ".mkd"]))
    assert(len(ps) > 1, "No posts returned")

def test_publish():
    assert(False)
