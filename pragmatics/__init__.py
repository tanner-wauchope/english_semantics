from plain_english.semantics.open_classes import (
    entity,
    text,
    number,
)
from plain_english.semantics import (
    open_classes,
    indefinite_article,
    definite_article,
    distributor,
    complementizer,
)


def populate_scope(scope):
    scope['a'] = indefinite_article.IndefiniteArticle(scope)
    scope['the'] = definite_article.DefiniteArticle(scope)
    scope['every'] = distributor.Distributor(scope)
    scope['that'] = complementizer.Complementizer(scope)
    scope['open_classes'] = {}
    scope['open_classes']['Entity'] = open_classes.Noun(noun=entity.Entity, scope=scope)
    scope['open_classes']['Text'] = open_classes.Noun(noun=text.Text, scope=scope)
    scope['open_classes']['Number'] = open_classes.Noun(noun=number.Number, scope=scope)
