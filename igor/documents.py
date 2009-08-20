from __future__ import with_statement

from os import path, makedirs
from datetime import datetime
from uuid import uuid4

import yaml
from git.log import Log

from markup import markup
from utils import slugify, compare_post_dates, relpath
from template_tools import render_template

documents = {}

class Document(object):
    def __init__(self, ref, id):
        self.type = self.__class__.__name__.lower()
        self.ref = ref
        self.id = id

        documents[id] = self

    def __repr__(self):
        return "<%s: %s %s>" % (self.type, self.id, self.ref)

class File(Document):
    _cached_contents = None

    def ref_data(self, ref):
        _, filename = path.split(ref)
        _, ext = path.splitext(ref)
        return (filename, ext)

    def contents(self, force=False):
        if not self._cached_contents or force:
            with open(self.ref, 'r') as f:
                return f.read()
        else:
            return self._cached_contents

class HeaderParser(object):
    def pop_section(self, lines):
        lines.reverse()
        section = []
        if lines:
            l = lines.pop()

            while l != "" and lines:
                section.append(l)
                l = lines.pop()

        lines.reverse()
        return ("\n".join(section).strip(), lines)

    def parse_time(self, time):
        try:
            return datetime.strptime(time, "%Y-%m-%d")
        except ValueError:
            try:
                return datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return datetime.now()

    def parse_headers(self, header):
        headers = yaml.load(header) or {}
        published_on = headers.get("published_on")

        if published_on:
            headers['published_on'] = self.parse_time(published_on)
        return headers

    def parse(self, contents):
        headers = {}
        lines = contents.splitlines()

        top, rest = self.pop_section(lines)

        if not rest:
            return (headers, "", "\n".join(top))

        if ":" in top:
            headers = self.parse_headers(top)
            title, rest = self.pop_section(rest)
        else:
            title = top

        return (headers, title, "\n".join(rest))

    def title_from_filename(self, filename):
        title, ext = path.splitext(filename)
        return slugify(title)

class Post(File, HeaderParser):
    """
    This class represents a document that will become a post in our blog. As
    such it makes certain assumptions about the kind of file it's been handed.
    It assumes that the file is formatted such that it has a header, title and
    body seperated by two newline characters, and at the current point in time
    it assumes that the file is part of a git project.
    """
    template = "post.html"
    index = "index.html"

    def __init__(self, ref, project_path="."):
        self.summary_cached = None

        self.project_path = path.abspath(project_path)
        self.ref = path.abspath(ref)
        self.filename, self.ext = self.ref_data(self.ref)
        self.headers, title, self.raw_body = self.parse(self.contents())
        self.body = self.markup_content(self.raw_body)

        self.title = self.headers.get('title') or title
        self.slug = self.headers.get('slug') or slugify(self.title) or self.title_from_filename(self.filename)
        self.git_log = Log(self.project_path, relpath(self.ref, self.project_path)).call()
        self.published_on = self.headers.get('published_on') or self.published_date()


        super(Post, self).__init__(ref, self.slug)

    def markup_content(self, content):
        return markup(self.ext)(content)

    def summary(self, length):
        return self.summary_cached or self.markup_content("\n".join(self.raw_body.splitlines()[:length]))
    
    def published_date(self):
        return self.git_log.headers['author'].datetime

    def author(self):
        return self.git_log.headers['author'].name

    def author_email(self):
        return self.git_log.headers['author'].email

    def publish_directory(self, date_format = "%Y/%m/%d"):
        return path.join(self.published_on.strftime(date_format), self.slug)

    def write(self):
        with open(self.ref, 'w') as f:
            header_content = yaml.dump(self.headers, default_flow_style=False)
            contents = "%s\n%s\n\n%s" % (header_content,
                                         self.title,
                                         self.raw_body)
            f.write(contents)
        return self

class Collection(Document):
    index = "index.html"
    template = "collection.html"
    slug = "collection"
    headers = {}

    def __init__(self, posts):
        super(Collection, self).__init__("", self.slug)

        posts.sort(compare_post_dates)
        self.posts = posts

    def publish_directory(self, date_format=""):
        return ""
        
class HomePage(Collection):
    template = "main.html"
    index = "index.html"
    slug = "home"

class Feed(Collection):
    template = "main.atom"
    index = "feed.atom"
    slug = "feed"

class Archive(Collection):
    template = "archive.html"
    index = "arvhive.html"
    slug = "archive"

def write(doc, env, publish_dir):
    out = render_template(doc, env, doc.template)
    publish_dir = path.join(publish_dir, doc.publish_directory())

    if not path.exists(publish_dir):
        makedirs(publish_dir) 

    publish_path = path.join(publish_dir, doc.index)

    print("... publishing: %s to %s" % (doc.slug, publish_path))

    with open(publish_path, 'w') as f:
        f.write(out)
