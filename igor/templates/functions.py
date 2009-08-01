from jinja2 import environmentfunction
from os import path
from urlparse import urljoin

functions = []

def join(base, ext):
    if base.startswith("http://"):
        return urljoin(base, ext)
    else:
        return path.join(base, ext)


@environmentfunction
def link_to(env, slug):
    docs = env.globals.get("documents")
    if docs:
        f_docs = [d for k,d in docs.iteritems() if k == slug]
        if f_docs:
            doc = f_docs[0]
            blog_uri = env.globals['config'].config.get("blog_uri")

            return join(blog_uri, doc.publish_directory())
    return ""
functions.append(link_to)
