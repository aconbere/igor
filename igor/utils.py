from re import sub
from os import path, listdir, remove
from shutil import copytree, copy2, rmtree

"""
Mostly this module includes files for wrapping copying, listing and filtering
files, these are for the most part just tools included in the standard
distribution, and non tested.

slugify is a little less like that and is in fact tested.
"""

def slugify(string):
    string = sub('\s+', '_', string)
    string = sub('[^\w.-]', '', string)
    return string.strip('_.- ').lower()

def hidden(p):
    """
    useful when using os.walk and relpath and want to know if a relative path is hidden.
    """
    return not (p == "." or p == "..") and p.startswith(".")

def relpath(long_path, base_path):
    """
    Emulates the bahaviour of path.relpath in py26 for use in cases where
    py26 or greater is unavailable. See documentation at.

    
    """
    if not hasattr(path, "relpath"):

       if not long_path.startswith(base_path):
           raise RuntimeError("Unexpected arguments")

       if long_path == base_path:
           return "."

       i = len(basePath)

       if not base_path.endswith(path.sep):
           i += len(path.sep)

       return long_path[i:]
    else:
        return path.relpath(long_path, base_path)

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
        remove(destination)
        copy2(source, destination)

def filter_dirs(source, filter):
    return [f for f in listdir(source) if filter(f)]

def list_dirs(source):
    return filter_dirs(source, lambda f: path.isdir(path.join(source, f)))

def list_files(source):
    return filter_dirs(source, lambda f: path.isfile(path.join(source, f)))
