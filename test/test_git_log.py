import sys
import os
from os import path
sys.path.append(".")

from igor.vcs.git.log import Log, Actor
from igor.vcs.git.refs import Ref

def test_log_parsing():
    test_git_log = """commit 108717603c6e6170e21c3b5334969acdd07843cb
    tree 6d1ffffbbff308420d0de0c5e2ebd3f02ad10186
    parent 45377d22fba89aa7a09540fc4f0ed9c921f6cf24
    author Anders Conbere <aconbere@gmail.com> 1248055489 -1000
    committer Anders Conbere <aconbere@gmail.com> 1248055489 -1000

        first run at the parser
    """

    log = Log("fake/dir")
    headers, comment = log.sections(test_git_log)
    hs = log.retreive_headers(headers)
    check_data = {
                  "commit": Ref("commit",
                                "108717603c6e6170e21c3b5334969acdd07843cb"),
                  "tree": Ref("tree",
                              "6d1ffffbbff308420d0de0c5e2ebd3f02ad10186"),
                  "parent": Ref("parent",
                                "45377d22fba89aa7a09540fc4f0ed9c921f6cf24"),
                  "author": Actor("author", "Anders Conbere",
                                  "aconbere@gmail.com", "1248055489", "1000"),
                  "committer": Actor("committer", "Anders Conbere",
                                     "aconbere@gmail.com", "1248055489", "1000")
                 }

    assert([(k, str(v)) for k,v in hs.iteritems()] == [(k,str(v)) for k,v in check_data.iteritems()])
    assert("\n".join(comment).strip() == "first run at the parser")

def test_log_retrieval(project):
    curdir = os.path.abspath(os.curdir)
    l = Log(project)
    headers, comment = l.call("_posts/welcome.txt")
    test_headers = {
                    "commit": Ref("commit",
                                  "4906ae03a875febcdc1fbd6b3d1d8d6f83ff309d"),
                    "tree": Ref("tree", "e3a8001f632e45275b018826623aaf8cdf53e707"),
                    "author": Actor("author", "Anders Conbere",
                                    "aconbere@gmail.com", "1248138252", "1000"),
                    "committer": Actor("committer", "Anders Conbere",
                                       "aconbere@gmail.com", "1248138252",
                                       "1000")
                   }
    assert(comment)
    header_keys = ["commit", "committer", "tree", "author"]
    assert([k for k,v in headers.iteritems()] == header_keys)
    
