import sys
from os import path
from shutil import rmtree

sys.path.append(".")

from igor.publisher import Publisher
from igor.documents import Post

def test_publisher(project):
    context = {}
    destination = "/tmp/blog.test"
    file = path.join(project, "_posts/welcome.txt")
    template_dir = path.join(project, "_templates")

    post = Post(file)
    p = Publisher([post], destination, template_dir, context)
    assert(p.publish())
    assert(path.exists(path.join(destination, post.publish_directory())))
    rmtree(destination)
