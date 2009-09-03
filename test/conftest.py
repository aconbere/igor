import sys
from shutil import rmtree
from os import path, chdir
from subprocess import check_call as call

sys.path.append(".")

from igor.tools import init

test_project = "/tmp/igor.test"
test_output = "/tmp/blog.test"

def initialize_test_project():
    try:
        rmtree(test_project)
    except:
        pass
    init(test_project)

    current_dir = path.abspath("")
    chdir(test_project)
    call(["git", "init"])
    call(["git", "add", "."])
    call(["git", "commit", "-m", "first commit"])
    chdir(current_dir)
    
    return test_project

def initialize_test_file():
    project = initialize_test_project()
    return path.join(project, "_posts/welcome.txt")

def teardown_test_project(a):
    try:
        rmtree(test_project)
    except:
        pass

def pytest_funcarg__project(request):
    return request.cached_setup(
        setup = initialize_test_project,
        teardown = teardown_test_project,
        scope = "module")

def pytest_funcarg__file(request):
    return request.cached_setup(
        setup = initialize_test_file,
        teardown = teardown_test_project,
        scope = "module")
    
