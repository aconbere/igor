from __future__ import with_statement

from os import path, makedirs
from datetime import datetime
from uuid import uuid4

import yaml
from git.log import Log

from markup import markup
from utils import slugify, relpath

class Document(object):
    documents = {}

    def __init__(self, ref, id):
        self.type = self.__class__.__name__.lower()
        self.ref = ref
        self.id = id
        self.documents[id] = self

    def __repr__(self):
        return "<%s: %s %s>" % (self.type, self.id, self.ref)

    @classmethod
    def clear(cls):
        cls.documents = {}
        return cls.all()

    @classmethod
    def all(cls):
        return cls.documents

    @classmethod
    def list(cls):
        return cls.documents.itervalues()

    @classmethod
    def filter(cls, slug):
        return [d for k,d in cls.documents.iteritems() if k == slug]


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

class Post(Document):
    """
    This class represents a document that will become a post in our blog. As
    such it makes certain assumptions about the kind of file it's been handed.
    It assumes that the file is formatted such that it has a header, title and
    body seperated by two newline characters, and at the current point in time
    it assumes that the file is part of a git project.
    """
    template = "post.html"
    out_file = "index.html"
    _cached_contents = None

    def __init__(self, ref, project_path="."):
        self.summary_cached = None

        self.project_path = path.abspath(project_path)
        self.ref = path.abspath(ref)
        self.filename, self.ext = self.ref_data(self.ref)
        self.headers, title, self.raw_body = HeaderParser().parse(self.contents())
        self.body = self.markup_content(self.raw_body)

        self.title = self.headers.get('title') or title
        self.slug = self.headers.get('slug') or slugify(self.title) or self.title_from_filename(self.filename)
        self.git_log = Log(self.project_path, relpath(self.ref, self.project_path)).call()
        self.published_on = self.headers.get('published_on') or self.published_date()
        super(Post, self).__init__(ref, self.slug)


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

    def markup_content(self, content):
        return markup(self.ext)(content)

    def summary(self, length):
        return self.summary_cached or self.markup_content("\n".join(self.raw_body.splitlines()[:length]))

    def title_from_filename(self, filename):
        title, ext = path.splitext(filename)
        return slugify(title)
    
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

    def __cmp__(self, p2):
        return cmp(p2.published_on, self.published_on)
        
class HomePage(Document):
    template = "main.html"
    out_file = "index.html"
    slug = "home"

    def __init__(self, posts):
        super(HomePage, self).__init__("", self.slug)
        posts.sort()
        self.posts = posts
        self.headers = {}

    def publish_directory(self):
        return ""

class Feed(Document):
    template = "main.atom"
    out_file = "feed.atom"
    slug = "feed"

    def __init__(self, posts):
        super(Feed, self).__init__("", self.slug)
        posts.sort()
        self.posts = posts
        self.headers = {}

    def publish_directory(self):
        return ""

class Archive(Document):
    template = "archive.html"
    out_file = "arvhive.html"
    slug = "archive"

    def __init__(self, posts):
        super(Archive, self).__init__("", self.slug)
        posts.sort()
        self.posts = posts
        self.headers = {}

    def publish_directory(self):
        return ""

    def organize_by_date(self, posts):
        # org[<year>][<month>][<day>]
        org = {}

        for post in posts:
            year = post.published_on.year
            month = post.published_on.month
            day = post.published_on.day

            if org.has_key(year):
                if org[year].has_key(month):
                    if org[year][month].has_key(day):
                        org[year][month][day].append(post)
                    else:
                        org[year][month][day] = []
                        org[year][month][day].append(post)
                else:
                    org[year][month] = {}
                    org[year][month][day] = []
                    org[year][month][day].append(post)
            else:
                org[year] = {}
                org[year][month] = {}
                org[year][month][day] = []
                org[year][month][day].append(post)
        return org

    def flatten_org(self):
        docs = []
        for y, ms in org:
            for m, ds in m:
                for d in m:
                    docs + d
        return docs

