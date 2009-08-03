from jinja2 import environmentfunction
from os import path
from urlparse import urljoin
from datetime import datetime
from time import mktime
from urlparse import urlparse

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
            blog_uri = env.globals['blog_url']

            return join(blog_uri, doc.publish_directory())
    return ""
functions.append(link_to)

def now():
    return datetime.now()
functions.append(now)

@environmentfunction
def tag_uri(env, post):
    blog_url = env.globals.get('blog_url')
    o = urlparse(blog_url)
    date = post.published_on.strftime("%Y-%m-%d")
    timestamp = mktime(post.published_on.timetuple())
    path = "tag:%s,%s:%s" % (o.netloc.replace("#", "/"), date, timestamp)
    return path
functions.append(tag_uri)
