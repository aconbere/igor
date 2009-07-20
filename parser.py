#!/usr/bin/env python
from __future__ import with_statement
from os import path
import simplejson as json

def remove_section(fd):
    section = ""
    l = fd.readline()

    while l != "\n":
        section += l
        l = fd.readline()

    return section

def remove_header(fd):
    return remove_section(fd)

def remove_title(fd):
    return remove_section(fd)

def parse_header(header):
    return json.loads(header)
    
def parse(file_name):
    with open(file_name, 'r') as f:
        data = parse_header(remove_header(f))
        data.update({"title": remove_title(f).strip()})
        data.update({"content": f.read().strip()})
    return data

def render(project_path, file_name):
    from jinja2 import Environment, FileSystemLoader
    data = parse(file_name)

    templates_path = path.abspath(path.join(project_path, '_templates'))
    env = Environment(loader=FileSystemLoader(templates_path))
    _template = data.get("_template") or "main.html"
    template = env.get_template(_template)
    return template.render(**data)

if __name__ == "__main__":
    from sys import argv
    print(render(argv[1], argv[2]))
