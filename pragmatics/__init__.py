from .a import IndefiniteArticle
from .the import DefiniteArticle
from .every import Distributor
from .nouns.entity import Entity
from .nouns.primitives.quote import Quote
from .nouns.primitives.number import Number

def new_scope(scope):
    scope['a'] = IndefiniteArticle(scope)
    scope['the'] = DefiniteArticle(scope)
    scope['every'] = Distributor(scope)
    scope['Entity'] = Entity
    scope['Quote'] = Quote
    scope['Number'] = Number
