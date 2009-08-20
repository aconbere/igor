from re import sub
from os import path, listdir
from shutil import copytree, copy2

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
       if not basePath.endswith(path.sep):
           i += len(path.sep)
       return longPath[i:]
    else:
        return path.relpath(longPath, basePath)

def copy_tree(source, destination):
    try:
        copytree(source, destination)
    except OSError:
        rmtree(destination)
        copytree(source, destination)

def copy_file(source, destination):
    try:
        copy2(source, destination)
    except OSError:
        
        

def filter_dirs(source, filter):
    return [f for f in listdir(dirname) if filter(f)]

def list_dirs(source):
    return filter_dirs(source, lambda f: path.isdir(os.path.join(source, f)))

def list_files(source):
    return filter_dirs(source, lambda f: path.isfile(os.path.join(source, f)))
