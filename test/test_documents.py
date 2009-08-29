import sys
import os

sys.path.append(".")

from igor.documents import Document, File, Post, HomePage, HeaderParser
from igor.utils import slugify

def test_document():
    d = Document("ref", 10)
    assert(d.ref == "ref")
    assert(d.id == 10)
    assert(d.type == "document")

def test_file():
    f = File("./examples/init/_posts/welcome.txt", 10)
    filename, ext = f.ref_data(f.ref)
    assert(filename == "welcome.txt")
    assert(ext == ".txt")

    contents = f.contents()
    assert(len(contents) > 0)

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
    file = "./examples/init/_posts/welcome.txt"
    p = Post(file, "./examples/init")
    assert(p.filename == "welcome.txt")
    assert(p.ext == ".txt")
    assert(p.title == "Welcome to your Igor blog")
    assert(p.raw_body.startswith("to start using igor"))
    assert(p.ref == file)
    assert(p.published_date())

def test_home_page():
    file = "./examples/init/_posts/welcome.txt"
    p = Post(file, "./examples/init")
    h = HomePage([p])
    assert(h)
