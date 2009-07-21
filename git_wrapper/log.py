from pyparsing import Word, alphas, alphanums, nums, Combine, Suppress, oneOf
from refs import Ref

from subprocess import PIPE, Popen

class Actor(object):
    roles = ["committer", "author"]

    def __init__(self, role, name, email, timestamp, offset):
        self.role = role
        self.name = name
        self.email = email
        self.timestamp = int(timestamp)

    def __repr__(self):
        return "<Actor: %s, %s, %s, %s>" % (self.role, self.name, self.email,
                                            self.timestamp)

    @classmethod
    def grammer(cls):
        _name = Combine(Word(alphanums) + " " + Word(alphanums))
        _email = Suppress("<") + Word(alphanums + "!#$%&'*+-/=?^_`{|}~@.") + Suppress(">")
        _timestamp = Word(nums)
        _offset = Combine("-" + Word(nums))
        return oneOf(cls.roles) + _name + _email + _timestamp + _offset

class Log(object):
    def __init__(self, filename):
        self.filename = filename
        self.stdout = PIPE
        self.headers = None
        self.comment = None

    def call(self):
        cmd = ["git", "log", "--all", "--diff-filter=A",
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
        return [self.parse_header(p) for p in headers]

    def parse_header(self, header):
        h = self.grammer().parseString(header.strip())
        if h[0] in Ref.refs:
            return Ref(h[0], h[1])
        elif h[0] in Actor.roles:
            return Actor(*h)
        
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
