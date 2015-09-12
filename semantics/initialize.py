from plain_english.semantics import (
    predicate,
    articles,
    primitive,
    modifiers,
)


def initialize(scope):
    scope['a'] = articles.An(scope)
    scope['an'] = scope['a']
    scope['the'] = articles.The(scope)
    scope['that'] = modifiers.That(scope)
    scope['nouns'] = {
        'Entity': predicate.OrderedSet('Entity', scope=scope),
        'Text': predicate.OrderedSet('Text', kind=primitive.Text, scope=scope),
        'Number': predicate.OrderedSet('Number', kind=primitive.Number, scope=scope),
        'File': predicate.OrderedSet('File', kind=primitive.File, scope=scope)
    }
    return scope
