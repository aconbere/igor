import sys
from os import path

sys.path.append(".")

from igor.markup import extensions, markup, NullProcessor, MarkdownProcessor,\
                        TextileProcessor

def test_extensions():
    known_exts = [".mkd", ".txt"]
    assert(all([ext in extensions() for ext in known_exts]))

def test_null_processor():
    test_string = "abcd\n\nxyc<a href=\"text\">a</a>\n\n###xyz###"
    n = NullProcessor()
    result = n.process(test_string)
    assert(result == test_string)

def test_markdown_processor():
    test_string = "abcd\n\nxyc<a href=\"text\">a</a>\n\n###xyz###"
    m = MarkdownProcessor()
    result = m.process(test_string)
    assert(result == '<p>abcd</p>\n<p>xyc<a href="text">a</a></p>\n<h3>xyz</h3>')


def test_textile_processor():
    test_string = "abcd\n\nxyc<a href=\"text\">a</a>\n\n###xyz###"
    t = TextileProcessor()
    result = t.process(test_string)
    assert(result == '\t<p>abcd</p>\n\n\t<p>xyc<a href="text">a</a></p>\n\n\t<p>###xyz###</p>')

def test_markup():
    test_string = "abcd\n\nxyc<a href=\"text\">a</a>\n\n###xyz###"
    result = markup(".mkd")(test_string)
    assert(result == '<p>abcd</p>\n<p>xyc<a href="text">a</a></p>\n<h3>xyz</h3>')
    
