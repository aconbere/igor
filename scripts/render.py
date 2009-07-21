#!/usr/bin/env python
import sys
from os import path

sys.path.append(path.abspath("."))

from blog_parser import ProjectParser


def main(project_path, out_path):
    ProjectParser(project_path, out_path).parse()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
