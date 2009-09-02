from pyparsing import Word, alphas, alphanums, nums, Combine, Suppress, oneOf
class Ref(object):
    refs = ["commit", "tree", "parent"]

    def __init__(self, name, ref):
        self.name = name
        self.ref = ref

    def __repr__(self):
        return "<Ref: %s, %s>" % (self.name, self.ref)

    @classmethod
    def grammer(cls):
        return oneOf(cls.refs) + Word(alphanums)
