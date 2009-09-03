from igor.utils import list_dirs
from git import Git
from os import path
from datetime import datetime

systems = {}

def type(project_path):
    dirs = list_dirs(project_path)
    if ".git" in dirs:
        return "git"
    elif ".hg" in dirs:
        return "hg"
    elif ".darcs" in dirs:
        return "darcs"
    elif ".svn" in dirs:
        return "svn"
    elif ".cvs" in dirs:
        return "cvs"
    return None

def get(type):
    for k,v in systems.iteritems():
        if k == type:
            return v
    return NullVCS

def register(type, cls):
    systems[type] = cls

class NullVCS(object):
    def __init__(self, text_file, project_path):
        self.text_file = text_file
        self.project_path = path.abspath(path.expanduser(project_path))

    def author(self):
        return ""

    def author_email(self):
        return ""

    def published_date(self):
        return datetime.now()

    def data(self):
        return {'author': self.author(),
                'author_email': self.author_email(),
                'published_date': self.published_date()}
register("none", NullVCS)
register("git", Git)
