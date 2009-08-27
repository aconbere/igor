from __future__ import with_statement

from os import walk, path, makedirs, removedirs
from jinja2 import Environment, FileSystemLoader
from shutil import copytree, rmtree

from documents import HomePage, Post, Feed, Archive, Document
from config import Config
from utils import hidden, relpath, list_dirs, list_files, copy_tree, copy_file
import markup

import template_tools

"""
This is the main module for igor, and provide the primary higher level tools
for actually publishing posts.
"""

def find_files(start_path, extensions=[".txt"]):
    """
    digs through a directory looksing for text files and directories
    that don't start in . or _
    """
    for file in list_files(start_path):
        name, ext= path.splitext(file)
        if not (file.startswith("_") or file.startswith(".")) and (ext in extensions):
            filename = path.join(start_path, file)
            yield filename

def make_posts(start_path, extensions=[".txt"]):
    """
    A simple wrapper around find_files, that filters on the markup extensions
    and returns each file to the Post class
    """
    return [Post(p, start_path) for p in find_files(start_path, extensions)] 

def copy_supporting_files(start_path, destination):
    for file in list_files(start_path):
        if not (file.startswith("_") or file.startswith(".")):
            print("copying: %s to: %s" % (file, destination))
            copy_file(path.join(start_path, file), path.join(destination, file))

    for dir in list_dirs(start_path):
        if not (dir.startswith("_") or dir.startswith(".")):
            print("copying: %s to: %s" % (dir, destination))
            copy_tree(path.join(start_path, dir), path.join(destination, dir))

def publish(source, destination=""):
    """
    Publishes all the posts found in _posts to destination
    """
    config = Config(source, destination)

    posts = make_posts(config.posts_dir, extensions=list(markup.extensions()))
    HomePage(posts)
    Feed(posts)
    Archive(posts)

    context = dict(documents = Document.all(), **config)

    publisher = Publisher(config.destination, config.templates_dir, context)
    [publisher.publish(d) for d in Document.all()]

    copy_supporting_files(config.source, config.destination)
