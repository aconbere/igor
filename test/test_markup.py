import sys
from os import path

sys.path.append(".")

from igor.markup import extensions, markup

def test_extensions():
    known_exts = [".mkd", ".txt"]
    assert(all([ext in extensions() for ext in known_exts]))
