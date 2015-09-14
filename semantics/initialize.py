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
    scope['singular'] = {
        'Entity': predicate.OrderedSet('Entity', scope=scope),
        'Text': predicate.OrderedSet('Text', kind=primitive.Text, scope=scope),
        'Number': predicate.OrderedSet('Number', kind=primitive.Number, scope=scope),
        'File': predicate.OrderedSet('File', kind=primitive.File, scope=scope)
    }
    scope['Entities'] = scope['singular']['Entity']
    scope['Texts'] = scope['singular']['Text']
    scope['Numbers'] = scope['singular']['Number']
    scope['Files'] = scope['singular']['File']
    return scope
