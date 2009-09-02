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

register("git", Git)
