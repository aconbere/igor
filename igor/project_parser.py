from os import walk, path, makedirs
from utils import hidden
from post import HomePage
from jinja2 import Environment, FileSystemLoader
from file_parser import FileParser
from helpers import link_to
from config import Config

class ProjectParser(object):
    template_dir = "_templates"
    posts_dir = "_posts"

    def __init__(self, project_path, out_dir=""):
        self.config = Config(path.join(project_path))

        print(out_dir)

        if out_dir:
            self.out_dir = out_dir
        elif self.config.get("output_directory"):
            self.out_dir = self.config.get("output_directory")
        else:
            raise Exception("output directory required")

        self.out_dir = path.abspath(path.expanduser(self.out_dir))

        self.project_path = path.abspath(project_path)
        self.posts_path = path.join(self.project_path, self.posts_dir)
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

    def set_globals(self):
        self.env.globals["link_to"] = link_to
        self.env.globals['posts'] = self.posts
        self.env.globals['config'] = self.config

    def write(self):
        self.posts.sort(
            lambda x,y: x.published_on > y.published_on)
        self.set_globals()

        HomePage(self.posts[:10]).write(self.env,
                                       self.out_dir)
        for post in self.posts:
            post.write(self.env, self.out_dir)
