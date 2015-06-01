from .the import DefiniteArticle
from .a import IndefiniteArticle


stack = [{}]
the = DefiniteArticle(stack)
a = an = IndefiniteArticle(stack)