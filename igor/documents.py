from os import path
from utils import slugify
from content_processors import markup
import yaml

documents = {}

class Document(object):
    def __init__(self, ref, id):
        self.type = self.__class__.__name__.lower()
        self.ref = ref
        self.id = id

        documents[id] = self

class File(Document):
    _cached_contents = None

    def ref_data(self, ref):
        _, filename = path.split(ref)
        ext = path.splitext(ref)
        return (filename, ext)

    def contents(self, force=False):
        if not self._cached_contents or force:
            with open(self.ref, 'r') as f:
                return f.read()
        else:
            return self._cached_contents

class PostParser(object):
    def pop_section(self, lines):
        section = []
        if lines:
            l = lines.pop()

            while l != "" and lines:
                section.append(l)
                l = lines.pop()

        return ("\n".join(section).strip(), lines) 

    def parse_headers(self, header):
        return yaml.load(header)

    def parse(self, contents):
        headers = {}
        lines = contents.splitlines()
        lines.reverse()

        top, rest = self.pop_section(lines)

        if not rest:
            return (headers, "", "\n".join(top))

        if ":" in top:
            headers = self.parse_headers(top)
            title, rest = self.pop_section(rest)
        else:
            title = top

        return (headers, title, "\n".join(rest))

    # consider moving this sort of stuff to
    # a meta data processor
    def get_published_date(self, data):
        datestr = data.get("published_on")

        if datestr:
            return datetime.strptime(datestr, "%Y-%m-%d")

        else:
            l = Log(self.project_path, self.relative_file_path)
            headers = l.call().headers
            return l.call().headers["author"].datetime

class Post(File, PostParser):
    def __init__(self, ref):
        self.ref = ref

        self.filename, self.ext = self.ref_data(self.ref)
        self.headers, title, body = self.parse(self.contents())
        self.body = self.markup_content(body)
        self.title = self.headers.get('title') or title
        self.slug = self.headers.get('slug') or slugify(self.title) or slugify(self.filename)
        super(Post, self).__init__(ref, self.slug)

    def markup_content(self, content):
        return markup(self.ext)(content)
