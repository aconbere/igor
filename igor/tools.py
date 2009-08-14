from __future__ import with_statement

from os import walk, path, makedirs, removedirs
from jinja2 import Environment, FileSystemLoader
from shutil import copytree, rmtree

from documents import HomePage, Post, Feed, Archive, write
from config import Config
from utils import hidden, relpath
import markup

import template_tools

template_dir = "_templates"
posts_dir = "_posts"
media_dir = "media"

def prepare_paths(source, destination):
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
    if not destination:
        raise Exception("Destination directory required")
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
    for (dirpath, dirnames, filenames) in walk(start_path):
        relative_path = relpath(dirpath, start_path)
        if not (relative_path.startswith("_") or hidden(relative_path)) and relative_path not in [".", ".."]:
            for filename in filenames:
                ext, name = path.splitext(filename)
                if not (filename.startswith("_") or hidden(filename)) and (ext in extensions):
                    file = path.join(start_path, dirpath, filename)
                    yield file

def find_posts(start_path, extensions=[".txt"]):
    return [Post(p, start_path) for p in find_files(start_path, markup.processors.iterkeys())]

def environment(templates_path, functions=[], filters=[], global_context={}):
    env = Environment(loader=FileSystemLoader(templates_path))
    [env.globals.__setitem__(f.func_name, f) for f in functions + template_tools.functions]
    [env.filters.__setitem__(f.func_name, f) for f in filters + template_tools.filters]
    env.globals.update(global_context)
    return env

def config(project_path):
    return Config(project_path)

def copy(source, destination):
    try:
        copytree(source, destination)
    except OSError:
        rmtree(destination)
        copytree(source, destination)

def copy_supporting_files(start_path, destination):
    special_directories = [".", ".."]
    for (dirpath, dirnames, filenames) in walk(start_path):
        relative_path = relpath(dirpath, start_path)
        if not (relative_path.startswith("_") or hidden(relative_path)) and (relative_path not in special_directories):
            source = path.join(start_path, dirpath)
            dest = path.join(destination, relative_path)
            print("copying: %s to: %s" % (source, dest))
            copy(path.join(start_path, dirpath), path.join(destination, relative_path))

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

def publish(source, destination):
    paths = prepare_paths(source, destination)
    config = Config(paths['source'])
    paths['destination'] = paths['destination'] or config.get("publish_directory")
    prepare_destination(paths['destination'])
    env = environment(paths['templates'], global_context=config)
    posts = find_posts(paths['posts'], markup.extensions())
    docs = posts + [HomePage(posts), Feed(posts), Archive(posts)]
    [write(doc, env, paths['destination']) for doc in docs]
    copy_supporting_files(paths['source'], paths['destination'])
