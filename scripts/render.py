#!/usr/bin/env python
import sys

sys.path.append(".")
sys.path.append("..")
sys.path.append("../..")

from parser import ProjectParser


def main(project_path, out_path):
    ProjectParser(project_path, out_path).parse()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
