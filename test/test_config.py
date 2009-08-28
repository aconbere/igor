import sys
import os

sys.path.append(".")

from igor.config import Config

def test_config():
    source = "./examples/init"
    destination = "~/blog"
    c = Config(source, destination)

    assert(c['author'] == "John Doe")
    assert(c['email'] == "jdoe@example.com")
    assert(c['blog_title'] == "Welcome to Igor")
    assert(c['publish_directory'] == "~/blog")
    assert(c['blog_url'] == "http://example.com/")
    assert(c['media_url'] == "http://media.example.com/")
    assert(c['summary_length'] == 10)
    assert(c['templates_prefix'] == "_templates")
    assert(c['posts_prefix'] == "_posts")
    assert(c.source.endswith("/examples/init"))
    assert(c.destination.endswith("blog"))
    assert(c.posts_dir)
    assert(c.templates_dir)
