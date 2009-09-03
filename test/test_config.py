import sys
from os import path
from shutil import rmtree

sys.path.append(".")

from igor.config import Config

def test_config(project):
    destination = "/tmp/blog.test"
    c = Config(project, destination).data()

    assert(c['author'] == "John Doe")
    assert(c['email'] == "jdoe@example.com")
    assert(c['blog_title'] == "Welcome to Igor")
    assert(c['destination'] == destination)
    assert(c['publish_dir'] == destination+"/") # no publish prefix
    assert(c['blog_url'] == "http://example.com/")
    assert(c['media_url'] == "http://media.example.com/")
    assert(c['summary_length'] == 10)
    assert(c['templates_prefix'] == "_templates")
    assert(c['posts_prefix'] == "_posts")
    assert(c['source'] == project)
    assert(c['posts_dir'])
    assert(c['templates_dir'])
