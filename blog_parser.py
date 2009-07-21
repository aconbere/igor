from os import walk, path, makedirs
from datetime import datetime

import yaml

from utils import slugify, hidden
from jinja2 import Environment, FileSystemLoader

from git_wrapper.log import Log

class ProjectParser(object):
    template_dir = "_templates"

    def __init__(self, project_path, out_dir):
        self.project_path = path.abspath(project_path)
        self.out_dir = path.abspath(out_dir)
        self.env = Environment(loader=FileSystemLoader(self.templates_path()))

    def templates_path(self):
        return path.abspath(path.join(self.project_path, self.template_dir))

    def parse(self, rebuild=False):
        if path.exists(self.out_dir):
            if rebuild:
                rmdir(out_dir)
        else:
            makedirs(self.out_dir)

        for (dirpath, dirnames, filenames) in walk(self.project_path):
            relative_path = path.relpath(dirpath, self.project_path)
            if not (relative_path.startswith("_") or hidden(relative_path)):
                for filename in filenames:
                    if not (filename.startswith("_") or hidden(filename)):
                        self.render_file(path.join(dirpath, filename), self.out_dir)

    def render_file(self, file_path, out_dir):
        post = FileParser(file_path, self.project_path)
        published_on = post.data["published_on"]
        out = post.render(self.env)

        sub_dir = path.join(out_dir, post.out_file_path())

        if not path.exists(sub_dir):
            makedirs(sub_dir)

        with open(path.join(sub_dir, post.index), 'w') as f:
            f.write(out)


class FileParser(object):
    default_template = "main.html"
    index = "index.html"

    def __init__(self, file_path, project_path):
        file_dir, filename = path.split(file_path)

        self.project_path = project_path
        self.relpath = path.relpath(file_path, project_path)
        self.file_path = file_path
        self.filename = filename
        self.data = self.parse(self.file_path)

    def _pop_section(self, fd):
        section = ""
        l = fd.readline()


        while l != "\n":
            section += l
            l = fd.readline()

        return section.strip()

    def parse_header(self, header):
        return yaml.load(header)

    def get_published_date(self, data):
        datestr = data.get("published_on")

        if datestr:
            return datetime.strptime(datestr, "%Y-%m-%d")

        else:
            l = Log(self.project_path, self.relpath)
            headers = l.call().headers
            print(headers)
            return l.call().headers["author"].datetime
            

    def parse(self, file_path):
        file_dir, filename = path.split(file_path)
        data = {}

        with open(file_path, 'r') as f:
            top = self._pop_section(f)
            data = {}
            title = top

            if ":" in top:
                data = self.parse_header(top)
                title = data.get("title") or self._pop_section(f)

            slug = data.get("slug") or slugify(title) or slugify(filename)

            published_on = self.get_published_date(data)
            last_modified = datetime.now()

            data.update({"title": title,
                         "slug": slug,
                         "published_on": published_on,
                         "last_modified": last_modified,
                         "content": f.read().strip()})
        return data

    def template(self):
        return self.data.get("template") or self.default_template

    def render(self, env):
        template = env.get_template(self.template())
        return template.render(**self.data)

    def out_file_path(self):
        date_path = self.data["published_on"].strftime("%Y/%m/%d/")
        return path.join(date_path, self.data["slug"])
