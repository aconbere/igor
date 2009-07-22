from os import walk, path, makedirs
from datetime import datetime

import yaml

from jinja2 import Environment, FileSystemLoader

from git_wrapper.log import Log
from utils import hidden
from post import Post, HomePage

class ProjectParser(object):
    template_dir = "_templates"
    posts_dir = "_posts"

    def __init__(self, project_path, out_dir):
        self.project_path = path.abspath(project_path)
        self.posts_path = path.join(self.project_path, self.posts_dir)
        self.out_dir = path.abspath(out_dir)
        self.env = Environment(loader=FileSystemLoader(self.templates_path()))
        self.posts = []

    def templates_path(self):
        return path.abspath(path.join(self.project_path, self.template_dir))

    def parse(self, rebuild=False):
        print("beginning parsing %s" % self.posts_path)

        if path.exists(self.out_dir):
            if rebuild:
                rmdir(out_dir)
        else:
            makedirs(self.out_dir)

        for (dirpath, dirnames, filenames) in walk(self.posts_path):
            relative_path = path.relpath(dirpath, self.posts_path)
            if not (relative_path.startswith("_") or hidden(relative_path)):
                for filename in filenames:
                    if not (filename.startswith("_") or hidden(filename)):
                        r = path.join(dirpath, filename)
                        relative_file_path = path.relpath(r, self.project_path)

                        post = FileParser(self.project_path,
                                          relative_file_path).parse()
                        self.posts.append(post)
        return self

    def write(self):
        self.posts.sort(lambda x,y: x.published_on > y.published_on)

        HomePage(self.posts[:10]).write(self.env, self.out_dir)

        for post in self.posts:
            post.write(self.env, self.out_dir)


class FileParser(object):
    default_template = "post.html"
    index = "index.html"

    def __init__(self, project_path, relative_file_path):
        """
            file_path is relative to project_path
        """
        self.project_path = project_path
        self.relative_file_path = relative_file_path

        _, self.filename = path.split(relative_file_path)

        self.file_path = path.join(self.project_path, self.relative_file_path)

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
            l = Log(self.project_path, self.relative_file_path)
            headers = l.call().headers
            return l.call().headers["author"].datetime
            

    def parse(self):
        file_dir, filename = path.split(self.file_path)
        data = {}

        with open(self.file_path, 'r') as f:
            data = {}
            top = self._pop_section(f)
            title = top

            if ":" in top:
                data = self.parse_header(top)
                title = data.get("title") or self._pop_section(f)

            return Post(title = title,
                        published_on = self.get_published_date(data),
                        last_modified = datetime.now(),
                        filename = filename,
                        content = f.read().strip(),
                        context = data)
