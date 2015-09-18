from plain_english.semantics import (
    predicate,
    articles,
    entities,
    modifiers,
)


def initialize(scope):
    indefinite_article = articles.IndefiniteArticle(scope)
    scope['a'] = indefinite_article
    scope['an'] = indefinite_article
    scope['the'] = articles.The(scope)
    scope['that'] = modifiers.That(scope)
    scope['Entities'] = predicate.OrderedSet(indefinite_article, 'Entity')
    scope['Texts'] = predicate.OrderedSet(indefinite_article, 'Text', kind=entities.Text)
    scope['Numbers'] = predicate.OrderedSet(indefinite_article, 'Number', kind=entities.Number)
    scope['Files'] = predicate.OrderedSet(indefinite_article, 'File', kind=entities.File)
    scope['singular'] = {
        'Entity': scope['Entities'],
        'Text': scope['Texts'],
        'Number': scope['Numbers'],
        'File': scope['Files']
    }
    return scope
