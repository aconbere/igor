import sys
from os import path

sys.path.append(".")

from igor.markup import extensions, markup

def test_extensions():
    known_exts = [".mkd", ".txt"]
    assert(all([ext in extensions() for ext in known_exts]))

def test_null_processor():
    test_string = "abcd\n\nxyc<a href=\"text\">a</a>\n\n###xyz###"
    n = NullProcessor()
    n.process(test_string)
    assert(n == test_string, "Null Processor Processed!")

def test_markdown_processor():
    assert(False)

def test_textile_processor():
    assert(False)

def test_markup():
    assert(False)
    
