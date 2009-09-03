import sys
import os

sys.path.append(".")

from igor.documents import Document, Post, HomePage, HeaderParser,\
                           find_document
from igor.utils import slugify

test_project = "./igor_extras/initial_project"
test_file = path.join(test_project, "_posts/welcome.txt")

def test_document():
    d = Document("slug")
    assert(d.slug == "slug")
    assert(d.type == "document")

def test_find_document():
    ds = [Document("a"), Document("slug"), Document("slug"),
          Document("b"), Document("c")]
    d = find_document([p], "slug")
    assert(d.slug = "slug")

def test_text_file():
    t = TextFile(test_file)
    assert(isinstance(t.headers, dict))
    assert(t.title)
    assert(t.body)

def test_text_file_pop_section():
    t = TextFile(test_file)
    top, rest = t.pop_section("this is the first section\n\nthis is the second\n\n".splitlines())
    assert(top == "this is the first section")

def test_text_file_parse():
    content = "this: 'is a header'\n\nwith a title\n\nand content"
    t = TextFile(test_file)
    headers, title, body = t.parse(content)
    assert(headers == {'this': 'is a header'})
    assert(title == "with a title")
    assert(body == "and content")

def test_post():
    p = Post(TextFile(test_file))
    assert(p.title)
    assert(p.slug)
    assert(p.filename)
    assert(p.ext)
    assert(p.markup())
    assert(p.summary(1))
    assert(p.published_date())
    assert(p.author())
    assert(p.author_email())

def test_home_page():
    f = "./examples/init/_posts/welcome.txt"
    p = Post(f, "./examples/init")
    h = HomePage([p])
    assert(h)
    assert(isinstance(h.headers, dict))
