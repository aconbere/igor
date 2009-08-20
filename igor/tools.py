from __future__ import with_statement

from os import walk, path, makedirs, removedirs
from jinja2 import Environment, FileSystemLoader
from shutil import copytree, rmtree

from documents import HomePage, Post, Feed, Archive, write, documents
from config import Config
from utils import hidden, relpath, list_dirs, list_files, copy_tree, copy_file
import markup

import template_tools

template_dir = "_templates"
posts_dir = "_posts"
media_dir = "media"

def prepare_paths(source, destination=""):
    source = path.abspath(path.expanduser(source))

    if destination:
        destination = path.abspath(path.expanduser(destination))

    return {
        "source": source,
        "destination": destination,
        "posts": path.join(source, posts_dir),
        "templates": path.join(source, template_dir),
        "media": path.join(source, media_dir),
        }

def prepare_destination(destination, rebuild=False):
    assert(destination, "Destination directory required")
    if path.exists(destination):
        if rebuild:
            rmtree(destination)
            makedirs(destination)
    else:
        makedirs(destination)

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

def find_posts(start_path, prefix="_posts", extensions=[".txt"]):
    print("start_path: %s" % start_path)
    print(list(find_files(path.join(start_path, prefix), extensions)))

    return [Post(p, start_path) for p in find_files(path.join(start_path, prefix), extensions)] 

def environment(templates_path, functions=[], filters=[], global_context={}):
    env = Environment(loader=FileSystemLoader(templates_path))
    [env.globals.__setitem__(f.func_name, f) for f in functions + template_tools.functions]
    [env.filters.__setitem__(f.func_name, f) for f in filters + template_tools.filters]
    env.globals.update(global_context)
    return env

def config(project_path):
    return Config(project_path)

def copy_supporting_files(start_path, destination):
    for file in list_files(start_path):
        if not (file.startswith("_") or file.startswith(".")):
            print("copying: %s to: %s" % (file, destination))
            copy_file(path.join(start_path, file), path.join(destination, file))

    for dir in list_dirs(start_path):
        if not (dir.startswith("_") or dir.startswith(".")):
            print("copying: %s to: %s" % (dir, destination))
            copy_tree(path.join(start_path, dir), path.join(destination, dir))

def organize_by_date(posts):
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

def flatten_org():
    docs = []
    for y, ms in org:
        for m, ds in m:
            for d in m:
                docs + d
    return docs

def publish(source, destination=""):
    paths = prepare_paths(source, destination)
    config = Config(paths['source'])

    paths['destination'] = paths['destination'] or config.get("publish_directory")
    assert(paths['destination'], "A destination directory is required")

    posts_path = path.join(paths['destination'], config.get("posts_prefix"))
    prepare_destination(paths['destination'])

    posts = find_posts(paths['source'], prefix=posts_dir, extensions=list(markup.extensions()))
    docs = posts + [HomePage(posts), Feed(posts), Archive(posts)]

    context = {'documents': documents}
    context.update(config)

    env = environment(paths['templates'], global_context=context)
    [write(doc, env, posts_path) for doc in docs]
    copy_supporting_files(paths['source'], paths['destination'])
