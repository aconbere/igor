from git import Git

systems = {None: BaseVCS}

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
    for k,v in systems:
        if k == type:
            return v
    return BaseVCS

def register(type, cls):
    systems[type] = cls

class BaseVCS(object):
    def __init__(self, text_file, project_path):
        self.text_file = text_file
        self.project_path = path.abspath(path.expanduser(project_path))

    def author(self):
        return ""

    def email(self):
        return ""

    def published_date(self):
        return datetime.now()

register("git", Git)
