from __future__ import with_statement

from os import path, makedirs
from datetime import datetime
from uuid import uuid4

import yaml
from git.log import Log

from markup import markup
from utils import slugify, relpath

def find_document(docs, slug):
    for d in docs:
        if d.slug == slug:
            return d

class Document(object):
    def __init__(self, slug):
        self.type = self.__class__.__name__.lower()
        self.slug = slug
        self.headers = {}

    def publish_directory(self):
        """
        by default publish to the destination root
        """
        return ""

    def __repr__(self):
        return "<%s: %s %s>" % (self.type, self.id, self.ref)

class TextFile(object):
    def __init__(self, file_path):
        self.file_path = path.abspath(file_path)
        _, self.filename = path.split(file_path)
        _, self.ext = path.splitext(file_path)
        self.headers, self.title, self.body = self.parse(self.read())

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

    def read(self, force=False):
        if not self._cached_contents or force:
            with open(self.ref, 'r') as f:
                return f.read()
        else:
            return self._cached_contents

    def write(self):
        with open(self.file_path, 'w') as f:
            header_content = yaml.dump(self.headers, default_flow_style=False)
            contents = "%s\n%s\n\n%s" % (header_content,
                                         self.title,
                                         self.raw_body)
            f.write(contents)
        return self


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
    _summary_cached = None
    _markup_cached = None

    def __init__(self, text_file, vcs):
        self.text_file = text_file
        self.vcs = vcs
        super(Post, self).__init__(self.slug())

    def title(self):
        return self.text_file.headers.get('title') or self.text_file.title

    def slug(self):
        title, _ = path.splitext(filename)
        return self.text_file.headers.get('slug') or slugify(self.title) or slugify(title)

    def body(self):
        if not self._markup_cached:
            return markup(self.text_file.ext)(self.text_file.body)
        else:
            return self._markup_cached

    def summary(self, length):
        if not self._summary_cached:
            return markup(self.text_file.ext)("\n".join(self.text_file.body.splitlines()[:length]))
        else:
            return self._summary_cached
    
    def published_date(self):
        header_published_date = self.text_file.headers.get('published_on'):
        return header_published_date or self.vcs.published_date()

    def author(self):
        headers_author = self.text_file.headers.get('author')
        return header_author or self.vcs.author()

    def author_email(self):
        header_email = self.text_file.headers.get('email')
        return header_email or self.vcs.author_email()

    def publish_directory(self, date_format = "%Y/%m/%d"):
        return path.join(self.published_date().strftime(date_format), self.slug())

    def __cmp__(self, p2):
        return cmp(p2.published_on, self.published_on)

class Collection(Document):
    def __init__(self, posts):
        posts.sort()
        self.posts = posts
        self.headers = {}
        super(Collection, self).__init__(self.slug)
        
class HomePage(Collection):
    template = "main.html"
    out_file = "index.html"
    slug = "home"

class Feed(Collection):
    template = "main.atom"
    out_file = "feed.atom"
    slug = "feed"

class Archive(Collection):
    template = "archive.html"
    out_file = "arvhive.html"
    slug = "archive"

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
