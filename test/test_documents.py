import sys
import os

sys.path.append(".")

from igor.documents import Document, File, Post, HomePage, PostParser
from igor.utils import slugify

def test_document():
    d = Document("ref", 10)
    assert(d.ref == "ref")
    assert(d.id == 10)
    assert(d.type == "document")

def test_file():
    f = File("./examples/basic/_posts/example.txt", 10)
    filename, ext = f.ref_data(f.ref)
    assert(filename == "example.txt")
    assert(ext == ".txt")

    contents = f.contents()
    assert(len(contents) > 0)

def test_post_parser_pop_section():
    p = PostParser()
    top, rest = p.pop_section("this is the first section\n\nthis is the second\n\n".splitlines())
    assert(top == "this is the first section")

def test_post_parser_parse():
    content = "this: 'is a header'\n\nwith a title\n\nand content"
    p = PostParser()
    headers, title, body = p.parse(content)
    assert(headers == {'this': 'is a header'})
    assert(title == "with a title")
    assert(body == "and content")

def test_post():
    file = "./examples/basic/_posts/example.txt"
    p = Post(file, "./examples/basic")
    assert(p.filename == "example.txt")
    assert(p.ext == ".txt")
    assert(p.title == "will default to the title text")
    print(p.raw_body)
    assert(p.raw_body.startswith("After that the rest is the content text."))
    assert(p.id == p.headers['slug'])
    assert(p.ref == file)
    assert(p.published_date())

def test_home_page():
    file = "./examples/basic/_posts/example.txt"
    p = Post(file, "./examples/basic")
    h = HomePage([p])
    assert(h)
