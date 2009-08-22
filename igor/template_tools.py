from rfc3339 import rfc3339
from jinja2 import environmentfunction
from os import path
from urlparse import urljoin
from datetime import datetime
from time import mktime
from urlparse import urlparse
from documents import Document

filters = []
functions = []

def date(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)
filters.append(date)

def rfc_date(value):
    return rfc3339(value)
filters.append(rfc_date)
    
def join(base, ext):
    if base.startswith("http://"):
        return urljoin(base, ext)
    else:
        return path.join(base, ext)

@environmentfunction
def link_to(env, slug):
    docs = Document.filter(slug)

    if docs:
        doc = docs[0]
        blog_path = join(env.globals['posts_prefix'], doc.publish_directory())
        blog_url = join(env.globals['blog_url'], blog_path)
        return blog_url

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

def render_template(doc, env, template_path):
    template = env.get_template(template_path)
    return template.render(doc=doc, **doc.headers)
