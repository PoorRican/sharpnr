from yaml import dump, load, YAMLObject
from random import randrange


STORAGE_FN = 'snippets.yaml'

class Reference(YAMLObject):
    yaml_tag = u'!Ref'
    def __init__(self, reference):
        # TODO: implement reference validation
        self.reference = reference

    def __str__(self):
        return self.reference

    def __unicode__(self):
        return u"%s" % self.reference

    def __repr__(self):
        return "%s(reference=%r)" % (
               self.__class__.__name__, self.reference)

class Snippet(YAMLObject):
    yaml_tag = u'!Snippet'
    db = []
    def __init__(self, reference, contents, version="ESV"):
        self._reference = Reference(reference)
        self.contents = contents
        self.version = version

        self.__class__.db.append(self)

    @property
    def reference(self):
        return self._reference.reference

    def __str__(self):
        return "%s - %s" % (self.contents, self.reference)

    def __unicode__(self):
        return u"%s - %s" % (self.contents, self.reference)

    def __repr__(self):
        return "%s(reference=%r, contents=%r, version=%r)" % (
               self.__class__.__name__, self._reference, self.contents, self.version)

    @classmethod
    def save(cls, fn=STORAGE_FN):
        with open(fn, 'w') as f:
            dump(cls.db, f)

    @classmethod
    def read(cls, fn=STORAGE_FN):
        with open(fn, 'r') as f:
            cls.db = load(f)

    @classmethod
    def random(cls):
        _max = len(cls.db)
        # TODO: implement array of previous selections to prevent repeats
        return cls.db[randrange(_max)]


Snippet.read(STORAGE_FN)
