import sys
from os import path

sys.path.append(".")

from igor.documents import Document, Post, HomePage, TextFile,\
                           find_document

def test_document():
    d = Document("slug")
    assert(d.slug == "slug")
    assert(d.type == "document")

def test_find_document():
    ds = [Document("a"), Document("slug"), Document("slug"),
          Document("b"), Document("c")]
    d = find_document(ds, "slug")
    assert(d.slug == "slug")

def test_text_file(file):
    t = TextFile(file)
    assert(isinstance(t.headers, dict))
    assert(t.title)
    assert(t.body)

def test_text_file_pop_section(file):
    t = TextFile(file)
    top, rest = t.pop_section("this is\nthe first section\n\nthis is the second\n\n".splitlines())
    assert(top == "this is\nthe first section")
    assert(rest == ["this is the second", ""])

def test_text_file_parse(file):
    content = "this: 'is a header'\ntitle: with a title\n\nand content"
    t = TextFile(file)
    headers, body = t.parse(content)
    title = headers.get("title")
    assert(headers == {'this': 'is a header', 'title': "with a title"})
    assert(body == "and content")

def test_post(file):
    p = Post(file)
    assert(p.title)
    assert(p.slug)
    assert(p.filename)
    assert(p.ext)
    assert(p.markup())
    assert(p.summary(1))
    assert(p.date())
    assert(p.author() == "")
    assert(p.author_email() == "")

def test_home_page(file):
    p = Post(file)
    h = HomePage([p])
    assert(h)
    assert(isinstance(h.headers, dict))
