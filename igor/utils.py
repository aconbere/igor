from re import sub
from os import path

def slugify(string):
    string = sub('\s+', '_', string)
    string = sub('[^\w.-]', '', string)
    return string.strip('_.- ').lower()

def hidden(p):
    return not (p == "." or p == "..") and p.startswith(".")

def compare_post_dates(p1, p2):
    return cmp(p2.published_on, p1.published_on)

def relpath(longPath, basePath):
    if not hasattr(path, "relpath"):
       if not longPath.startswith(basePath):
           raise RuntimeError("Unexpected arguments")
       if longPath == basePath:
           return "."
       i = len(basePath)
       if not basePath.endswith(os.path.sep):
           i += len(os.path.sep)
       return longPath[i:]
    else:
        return path.relpath(longPath, basePath)
