import sys
from os import path

sys.path.append(".")

from igor.publisher import Publisher
from igor.documents import Post

test_dest = "/tmp/igor.test"
test_template_dir = "./examples/init/_templates"
test_context = {} 

def test_publisher():
    p = Publisher(test_dest, test_template_dir, test_context)
    post = Post("./examples/init/_posts/welcome.txt", "./examples/init")
    p.publish(post)
    assert(path.exists(path.join(test_dest, post.publish_directory())))
