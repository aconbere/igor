from __future__ import with_statement

from os import path, makedirs
from datetime import datetime
from uuid import uuid4

import yaml

from vcs.git.log import Log
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
        return "<%s: %s>" % (self.type, self.slug)

class TextFile(object):
    def __init__(self, file_path):
        self._cached_contents = None
        self.file_path = path.abspath(file_path)
        self.headers, self.body = self.parse(self.read(self.file_path))
        self.title = self.headers.get("title") or ""

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

        if headers.__class__ == str:
            headers = {"title": headers}
            return headers

        date = headers.get("date")

        if date:
            headers['date'] = self.parse_time(date)

        return headers

    def parse(self, contents):
        headers = {"title": ""}
        lines = contents.splitlines()

        top, rest = self.pop_section(lines)

        if not rest:
            rest = top
        else:
            headers = self.parse_headers(top)

        return (headers, "\n".join(rest))

    def read(self, file_path, force=False):
        if not self._cached_contents or force:
            with open(file_path, 'r') as f:
                return f.read()
        else:
            return self._cached_contents

    def write(self):
        with open(self.file_path, 'w') as f:
            header_content = yaml.dump(self.headers(), default_flow_style=False)
            contents = "%s\n%s\n\n%s" % (header_content,
                                         self.body)
            f.write(contents)
        return self

def make_post(file_path, project_path, vcs_type=None):
    vcs_type = vcs_type or vcs.type(project_path)
    vcs = vcs.get(vcs_type)
    


class Post(Document):
    """
    This class represents a document that will become a post in our blog. 
    """
    template = "post.html"
    out_file = "index.html"
    _summary_cached = None
    _markup_cached = None

    def __init__(self, file_path, extra_data={}):
        self.text_file = TextFile(file_path)
        self.title = self.text_file.title
        self.extra_data = extra_data
        self.filename, self.ext = path.splitext(self.text_file.file_path)
        self.slug = self.text_file.headers.get('slug') or slugify(self.title) or \
                                                          slugify(self.filename)
        self.body = self.markup()

        super(Post, self).__init__(self.slug)
        self.headers = self.text_file.headers

    def markup(self):
        if not self._markup_cached:
            return markup(self.ext)(self.text_file.body)
        else:
            return self._markup_cached

    def summary(self, length):
        if not self._summary_cached:
            return markup(self.ext)("\n".join(self.text_file.body.splitlines()[:length]))
        else:
            return self._summary_cached
    
    def date(self):
        header_date = self.headers.get('date')
        return header_date or self.extra_data.get('date') or \
               datetime.now()

    def author(self):
        header_author = self.text_file.headers.get('author')
        return header_author or self.extra_data.get('author') or ""

    def author_email(self):
        header_email = self.text_file.headers.get('email')
        return header_email or self.extra_data.get('author_email') or ""

    def publish_directory(self, date_format = "%Y/%m/%d"):
        return path.join(self.date().strftime(date_format),
                         self.slug)

    def __cmp__(self, p2):
        return cmp(p2.date(), self.date())

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
    out_file = "index.html"
    slug = "archive"

    def __init__(self, posts):
        super(Archive, self).__init__(posts)
        self.posts = self.organize_by_date(self.posts)

    def publish_directory(self):
        return "archive/"

    def organize_by_date(self, posts):
        # org[<year>][<month>][<day>][<post>]
        org = {}

        for post in posts:
            year = post.date().year
            month = post.date().month
            day = post.date().day

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
