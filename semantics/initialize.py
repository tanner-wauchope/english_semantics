from plain_english.semantics import (
    predicate,
    articles,
    primitive,
    modifiers,
)


def initialize(scope):
    scope['a'] = articles.IndefiniteArticle(scope)
    scope['an'] = scope['a']
    scope['the'] = articles.The(scope)
    scope['that'] = modifiers.That(scope)
    scope['Entities'] = predicate.OrderedSet('Entity', scope=scope)
    scope['Texts'] = predicate.OrderedSet('Text', kind=primitive.Text, scope=scope)
    scope['Numbers'] = predicate.OrderedSet('Number', kind=primitive.Number, scope=scope)
    scope['Files'] = predicate.OrderedSet('File', kind=primitive.File, scope=scope)
    scope['singular'] = {
        'Entity': scope['Entities'],
        'Text': scope['Texts'],
        'Number': scope['Numbers'],
        'File': scope['Files']
    }
    return scope
