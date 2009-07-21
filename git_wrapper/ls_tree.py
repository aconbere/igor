from pyparsing import Word, alphas, alphanums, nums, Combine, Suppress, oneOf
from subprocess import Popen, PIPE

class ListElement(object):
    def __init__(self, id, type, hash, filename):
        self.id = id
        self.type = type
        self.hash = hash
        self.filename = filename

    @classmethod
    def grammer(cls):
        _id = Word(nums)
        _type = Word(alphas)
        _hash = Word(alphanums)
        _filepath = Word(alphanums+"._-+ ~<>*/")
        return _id + _type + _hash + _filepath

    @classmethod
    def from_string(cls, string):
        l = cls.grammer().parseString(string)
        return cls(l[0], l[1], l[2], l[3])

    def __repr__(self):
        return "<ListElement: %s %s %s %s>" % (self.id, self.type, self.hash, self.filename)
        

class ListTree(object):
    stdout = PIPE
    def __init__(self):
        self.out = None
        self.elements = None

    def call(self):
        cmd = ["git", "ls-tree", "-r", "HEAD"]
        p = Popen(cmd, stdout = self.stdout)
        p.wait()

        if p.returncode != 0:
            print("freakout!")

        self.out = p.stdout.read()
        self.elements = self.parse_list(self.out)
        return self

    def parse_list(self, out):
        return [ListElement.from_string(l) for l in out.splitlines() if l.strip()]
