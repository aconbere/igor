import sys
import os

sys.path.append(".")

from igor.documents import Document, Post, HomePage, HeaderParser,\
                           find_document
from igor.utils import slugify

def test_document():
    d = Document("slug")
    assert(d.slug == "slug")
    assert(d.type == "document")

def test_find_document():
    f = "./examples/init/_posts/welcome.txt"
    p = Post(f, "./examples/init")
    find_document([p], "welcome")

def test_post_parser_pop_section():
    p = HeaderParser()
    top, rest = p.pop_section("this is the first section\n\nthis is the second\n\n".splitlines())
    assert(top == "this is the first section")

def test_post_parser_parse():
    content = "this: 'is a header'\n\nwith a title\n\nand content"
    p = HeaderParser()
    headers, title, body = p.parse(content)
    assert(headers == {'this': 'is a header'})
    assert(title == "with a title")
    assert(body == "and content")

def test_post():
    f = "./examples/init/_posts/welcome.txt"
    p = Post(f, "./examples/init")
    assert(p.filename == "welcome.txt")
    assert(p.ext == ".txt")
    assert(p.title == "Welcome to your Igor blog")
    assert(p.raw_body.startswith("to start using igor"))
    assert(p.ref == os.path.abspath(f))
    assert(p.published_date())
    assert(isinstance(p.headers, dict))

def test_home_page():
    f = "./examples/init/_posts/welcome.txt"
    p = Post(f, "./examples/init")
    h = HomePage([p])
    assert(h)
    assert(isinstance(h.headers, dict))
