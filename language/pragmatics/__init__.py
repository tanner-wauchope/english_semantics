from .a import IndefiniteArticle
from .the import DefiniteArticle
from .each import Distributor

def new_scope(scope):
    scope['a'] = IndefiniteArticle(scope)
    scope['the'] = DefiniteArticle(scope)
    scope['each'] = Distributor(scope)
