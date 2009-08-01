from __future__ import with_statement

from os import walk, path, makedirs, removedirs
from jinja2 import Environment, FileSystemLoader
from shutil import copytree, rmtree

from documents import HomePage, Post
from config import Config
from utils import hidden, relpath
from publish import publish

from templates.functions import functions
from templates.filters import filters

class ProjectParser(object):
    template_dir = "_templates"
    posts_dir = "_posts"
    media_dir = "_media"

    def __init__(self, project_path, publish_dir=""):
        self.config = Config(path.join(project_path))

        publish_dir = publish_dir or self.config.get("publish_directory")
        if not publish_dir:
            raise Exception("output directory required")

        self.publish_dir = path.abspath(path.expanduser(publish_dir))

        self.project_path = path.abspath(project_path)
        self.posts_path = path.join(self.project_path, self.posts_dir)
        self.templates_path = path.abspath(path.join(self.project_path,
                                           self.template_dir))
        self.media_path = path.abspath(path.join(self.project_path,
                                           self.media_dir))
        self.posts = []

    def set_environment(self):
        self.env = Environment(loader=FileSystemLoader(self.templates_path))
        [self.env.globals.__setitem__(f.func_name, f) for f in functions]
        [self.env.filters.__setitem__(f.func_name, f) for f in filters]
        self.env.globals['posts'] = self.posts
        self.env.globals['config'] = self.config
        self.env.globals['blog_title'] = self.config.get('blog_title')

    def prepare_output_directory(self, rebuild=False):
        if path.exists(self.publish_dir):
            if rebuild:
                rmtree(publish_dir)
        else:
            makedirs(self.publish_dir)

    def copy_media(self):
        print("copying media...")
        media_path = path.join(self.project_path, self.media_dir)
        out_path = path.join(self.publish_dir, "media")
        try:
            copytree(media_path, out_path)
        except OSError:
            rmtree(out_path)
            copytree(media_path, out_path)

    def collect_post_files(self):
        """
        digs through a directory looksing for text files and directories
        that don't start in . or _
        """
        print("Collecting posts...")
        posts = []

        for (dirpath, dirnames, filenames) in walk(self.posts_path):
            relative_path = relpath(dirpath, self.posts_path)
            if not (relative_path.startswith("_") or hidden(relative_path)):
                for filename in filenames:
                    if not (filename.startswith("_") or hidden(filename)):
                        file = path.join(self.posts_path, dirpath, filename)
                        posts.append(file)
        return posts

    def get_posts(self):
        self.posts = [Post(p, self.project_path) for p in self.collect_post_files()]
        return self.posts

    def organize_posts_by_date(self, posts):
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


    def write(self, rebuild=False):
        self.get_posts()
        self.prepare_output_directory(rebuild)
        self.set_environment()

        for post in self.posts:
            publish(post, self.env, self.publish_dir)

        home_page = HomePage(self.posts)
        publish(home_page, self.env, self.publish_dir)
        self.copy_media()
