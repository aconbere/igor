import sys
import os
from pkg_resources import resource_filename

sys.path.append(".")

from igor.config import Config

def test_config():
    source = "./igor_extras/initial_project"
    destination = "/tmp/igor_unit_tests"
    c = Config(source, destination).data()

    assert(c['author'] == "John Doe")
    assert(c['email'] == "jdoe@example.com")
    assert(c['blog_title'] == "Welcome to Igor")
    assert(c['destination'] == destination)
    assert(c['publish_dir'].endswith("blog/"))
    assert(c['blog_url'] == "http://example.com/")
    assert(c['media_url'] == "http://media.example.com/")
    assert(c['summary_length'] == 10)
    assert(c['templates_prefix'] == "_templates")
    assert(c['posts_prefix'] == "_posts")
    assert(c['source'].endswith("/igor_extras/initial_project"))
    assert(c['posts_dir'])
    assert(c['templates_dir'])
