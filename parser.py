#!/usr/bin/env python
from __future__ import with_statement
from os import path, walk
import simplejson as json
import yaml

def slugify(string):
    string = re.sub('\s+', '_', string)
    string = re.sub('[^\w.-]', '', string)
    return string.strip('_.- ').lower()

def remove_section(fd):
    section = ""
    l = fd.readline()

    while l != "\n":
        section += l
        l = fd.readline()

    return section.strip()

def remove_header(fd):
    return remove_section(fd)

def remove_title(fd):
    return remove_section(fd)

def parse_header(header):
    return yaml.load(header)
    
def parse(filename):
    data = {}
    with open(filename, 'r') as f:
        data = parse_header(remove_header(f))

        title = data.get("title") or remove_title(f)
        slug = data.get("slug") or slugify(title) or slugify(filename)
        published_on = date.strptime(data.get("published_on"), "%Y-%m-%d")
        last_modified = date.strptime(data.get("last_modified"), "%Y-%m-%d")

        data.update({"title": title,
                     "slug": slug,
                     "published_on": published_on,
                     "last_modified": last_modified,
                     "content": f.read().strip()})
    return data

def render(project_path, filename, data):
    from jinja2 import Environment, FileSystemLoader

    templates_path = path.abspath(path.join(project_path, '_templates'))
    env = Environment(loader=FileSystemLoader(templates_path))
    _template = data.get("_template") or "main.html"
    template = env.get_template(_template)
    return template.render(**data)

def parse_project(project_path):
    for (dirpath, dirnames, filenames) in walk(project_path):
        if not dirpath.startswith("_"):
            for filename in filenames:
                if not filename.startswith("_"):
                    data = parse(filename)
                    out = render(project_path, filename, data)
                    new_file_name = 
    

if __name__ == "__main__":
    from sys import argv
    print(render(argv[1], argv[2]))
