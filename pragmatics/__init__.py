from plain_english.pragmatics.text import text
from plain_english.pragmatics.numbers import number
from plain_english.semantics import nouns, entity
from plain_english.semantics.function_words import (
    indefinite_article,
    definite_article,
    distributor,
    complementizer,
)


def populate_scope(scope):
    scope['a'] = indefinite_article.IndefiniteArticle(scope)
    scope['the'] = definite_article.DefiniteArticle(scope)
    scope['every'] = distributor.Distributor(scope)
    scope['that'] = complementizer.Complementizer()
    scope['nouns'] = {}
    scope['nouns']['Entity'] = nouns.Group(noun=entity.Entity, scope=scope)
    scope['nouns']['Text'] = nouns.Group(noun=text.Text, scope=scope)
    scope['nouns']['Number'] = nouns.Group(noun=number.Number, scope=scope)
