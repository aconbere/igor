from os import walk, path
from datetime import datetime

import simplejson as json
import yaml

from utils import slugify, hidden
from jinja2 import Environment, FileSystemLoader


# output directories should look something like
# /posts/Y/M/D/slug/index.html


class ProjectParser(object):
    def __init__(self, project_path, out_path):
        self.project_path = path.abspath(project_path)
        self.out_path = path.abspath(out_path)

    def parse(self):
        filepaths = []
        for (dirpath, dirnames, filenames) in walk(self.project_path):
            relative_path = path.relpath(dirpath, self.project_path)
            if not (relative_path.startswith("_") or hidden(relative_path)):
                for filename in filenames:
                    if not (filename.startswith("_") or hidden(filename)):
                        print(path.join(dirpath, filename))
                        parsed_file = FileParser(path.join(dirpath, filename))
                        out = render(self.project_path, parsed_file.filename,
                                     parsed_file.data)
                        
#                        print(out)

class FileParser(object):
    def __init__(self, filename):
        self.filename = filename
        self.data = self._parse(self.filename)        

    def _pop_section(self, fd):
        section = ""
        l = fd.readline()


        while l != "\n":
            section += l
            l = fd.readline()

        return section.strip()

    def _parse_header(self, header):
        return yaml.load(header)

    def _parse(self, filename):
        data = {}
        with open(filename, 'r') as f:
            top = self._pop_section(f)
            data = {}
            title = top

            if ":" in top:
                data = self._parse_header(top)
                title = data.get("title") or self._pop_section(f)

            slug = data.get("slug") or slugify(title) or slugify(filename)
            published_on = datetime.strptime(data.get("published_on"), "%Y-%m-%d")
            last_modified = datetime.strptime(data.get("last_modified"), "%Y-%m-%d")

            data.update({"title": title,
                         "slug": slug,
                         "published_on": published_on,
                         "last_modified": last_modified,
                         "content": f.read().strip()})
        return data

def render(project_path, filename, data):
    templates_path = path.abspath(path.join(project_path, '_templates'))
    env = Environment(loader=FileSystemLoader(templates_path))
    _template = data.get("_template") or "main.html"
    template = env.get_template(_template)
    return template.render(**data)
