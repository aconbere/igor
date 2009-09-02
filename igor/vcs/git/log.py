from pyparsing import Word, alphas, alphanums, nums, Combine, Suppress, oneOf
from refs import Ref
from os import path

from subprocess import PIPE, Popen
from datetime import datetime

class Actor(object):
    roles = ["committer", "author"]

    def __init__(self, role, name, email, timestamp, offset):
        self.role = role
        self.name = name
        self.email = email
        self.timestamp = int(timestamp)
        self.datetime= datetime.fromtimestamp(self.timestamp)

    def __repr__(self):
        return "<Actor: %s, %s, %s, %s>" % (self.role, self.name, self.email,
                                            self.timestamp)

    @classmethod
    def grammer(cls):
        _name = Combine(Word(alphanums) + " " + Word(alphanums))
        _email = Suppress("<") + Word(alphanums + "!#$%&'*+-/=?^_`{|}~@.") + Suppress(">")
        _timestamp = Word(nums)
        _offset = Combine(Word("-+") + Word(nums))
        return oneOf(cls.roles) + _name + _email + _timestamp + _offset

class Log(object):
    stdout = PIPE

    def __init__(self, git_dir, filename):
        self.git_dir = git_dir
        self.filename = filename
        self.headers = {}
        self.comment = None

    def call(self):
        git_dir_opt = "--git-dir=%s" % path.join(self.git_dir, ".git")
        cmd = ["git", git_dir_opt, "log", "--all", "--diff-filter=A",
              "--pretty=raw", "--", self.filename]
        p = Popen(cmd, stdout = self.stdout)
        p.wait()

        if p.returncode != 0:
            print("freakout!")

        else:
            out = p.stdout.read()
            headers, comment = self.sections(out)
            self.headers = self.retreive_headers(headers)
            self.comment = "\n".join(comment).strip()
        return self

    @classmethod
    def grammer(cls):
        return (Actor.grammer() | Ref.grammer())
        
    def retreive_headers(self, headers):
        return dict([self.parse_header(p) for p in headers])

    def parse_header(self, header):
        h = self.grammer().parseString(header.strip())
        if h[0] in Ref.refs:
            r =  Ref(h[0], h[1])
            return (r.name, Ref(h[0], h[1]))
        elif h[0] in Actor.roles:
            a = Actor(*h)
            return (a.role, Actor(*h))
        
    def sections(self, log):
        lines = log.splitlines()
        headers = []
        comment = ""

        for (i, l) in enumerate(lines):
            l = l.strip()
            if l == "":
                comment = lines[i+1:]
                break
            headers.append(l)
        return (headers, comment)
