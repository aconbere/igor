import sys
import os
sys.path.append("..")
sys.path.append(".")

from git_wrapper.log import Log, Actor
from git_wrapper.refs import Ref

def test_log_parsing():
    test_git_log = """commit 108717603c6e6170e21c3b5334969acdd07843cb
    tree 6d1ffffbbff308420d0de0c5e2ebd3f02ad10186
    parent 45377d22fba89aa7a09540fc4f0ed9c921f6cf24
    author Anders Conbere <aconbere@gmail.com> 1248055489 -1000
    committer Anders Conbere <aconbere@gmail.com> 1248055489 -1000

        first run at the parser
    """

    log = Log("fake_file")
    headers, comment = log.sections(test_git_log)
    hs = log.retreive_headers(headers)
    check_data = [Ref("commit","108717603c6e6170e21c3b5334969acdd07843cb"),
                  Ref("tree", "6d1ffffbbff308420d0de0c5e2ebd3f02ad10186"),
                  Ref("parent", "45377d22fba89aa7a09540fc4f0ed9c921f6cf24"),
                  Actor("author", "Anders Conbere", "aconbere@gmail.com", "1248055489", "1000"),
                  Actor("committer", "Anders Conbere", "aconbere@gmail.com", "1248055489", "1000"),]

    assert([str(h) for h in hs] == [str(c) for c in check_data])
    assert("\n".join(comment).strip() == "first run at the parser")

def test_log_retrieval():
    os.chdir("test/example")
    l = Log("example.txt")
    l.call()
    test_headers = [Ref("commit", "4906ae03a875febcdc1fbd6b3d1d8d6f83ff309d"),
                    Ref("tree", "e3a8001f632e45275b018826623aaf8cdf53e707"),
                    Actor("author", "Anders Conbere", "aconbere@gmail.com", "1248138252", "1000"),
                    Actor("committer", "Anders Conbere", "aconbere@gmail.com", "1248138252", "1000"),]
    assert(l.comment == "first commit")
    assert([str(h) for h in l.headers] == [str(t) for t in test_headers])
    
