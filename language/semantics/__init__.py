from .all_ import UniversalQuantifier
from .the import DefiniteArticle
from .a import IndefiniteArticle
from .that import Complementizer
from . import verbs

all_ = UniversalQuantifier()
the = DefiniteArticle(all_)
a = an = IndefiniteArticle(the, all_)
that = Complementizer()
