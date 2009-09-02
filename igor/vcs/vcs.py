from git import Git

systems = {}

def vcs_type(project_path):
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

def get_vcs(type):
    for k,v in systems:
        if k == type:
            return v
    return None

def register(type, cls):
    systems[type] = cls

class BaseVCS(object):
    def __init__(self, project_path, file_path):
        self.project_path = project_path
        self.file_path = file_path

    def publish_date():
        raise Exception("publish_date not implimented")

    def author():
        raise Exception("publish_date not implimented")

    def author_email():
        raise Exception("publish_date not implimented")

register("git", Git)
