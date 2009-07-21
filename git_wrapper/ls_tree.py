from pyparsing import Word, alphas, alphanums, nums, Combine, Suppress, oneOf
from subprocess import Popen, PIPE

class ListElement(object):
    def __init__(self, type, hash, filename):
        self.type = type
        self.hash = hash
        self.filename = filename

    @classmethod
    def grammer(cls):
        _type = Word(alphas)
        _hash = Word(alphanums)
        _filename = Word(alphanums, "._-+ ~<>*")
        return Word(nums) + _type + _hash + _filename

    @classmethod
    def from_string(cls, string):
        l = cls.grammer.parseString(string)
        return cls(l[0], l[1], l[2])
        

class ListTree(object):
    def call(self):
        cmd = ["git", "ls-tree", "HEAD"]
        p = Popen(cmd, stdout = self.stdout)
        p.wait()
        if p.returncode != 0:
            print("freakout!")
        else:
            out = p.stdout.read()
            self.elements = [ListElement.from_string(l) for l in out if l.strip()]
        return self
