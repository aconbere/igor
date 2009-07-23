from os import walk, path, makedirs, removedirs
from utils import hidden, compare_post_dates
from post import HomePage
from jinja2 import Environment, FileSystemLoader
from file_parser import FileParser
from helpers import link_to
from config import Config
from shutil import copytree, rmtree

class ProjectParser(object):
    template_dir = "_templates"
    posts_dir = "_posts"
    media_dir = "_media"

    def __init__(self, project_path, out_dir=""):
        self.config = Config(path.join(project_path))

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

    def prepare_output_directory(self, rebuild=False):
        if path.exists(self.out_dir):
            if rebuild:
                rmtree(out_dir)
        else:
            makedirs(self.out_dir)

    def collect_media(self):
        print("copying media...")
        media_path = path.join(self.project_path, self.media_dir)
        out_path = path.join(self.out_dir, "media")
        try:
            copytree(media_path, out_path)
        except OSError:
            rmtree(out_path)
            copytree(media_path, out_path)
            

    def parse(self, rebuild=False):
        print("beginning parsing %s" % self.posts_path)

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
        self.prepare_output_directory()
        self.posts.sort(compare_post_dates)
        
        self.set_globals()

        ps = sorted(self.posts, compare_post_dates)
        print(ps)
        HomePage(self.posts[:10]).write(self.env,
                                       self.out_dir)
        for post in self.posts:
            post.write(self.env, self.out_dir)
        self.collect_media()
