#!/usr/bin/env python
from sys import argv
from parser import ProjectParser

def main(project_path):
    ProjectParser(project_path).parse()

if __name__ == "__main__":
    main(argv[1])
