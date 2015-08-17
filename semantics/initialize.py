from plain_english.semantics import (
    predicate,
    determiners,
    primitive,
)


def initialize(scope):
    scope['a'] = determiners.An(scope)
    scope['an'] = determiners.An(scope)
    scope['the'] = determiners.The(scope)
    scope['all'] = determiners.All(scope)
    scope['that'] = predicate.That(scope)
    scope['nouns'] = {
        'Entity': predicate.OrderedSet('Entity', scope=scope),
        'Text': predicate.OrderedSet('Text', kind=primitive.Text, scope=scope),
        'Number': predicate.OrderedSet('Number', kind=primitive.Number, scope=scope),
        'File': predicate.OrderedSet('File', kind=primitive.File, scope=scope)
    }
    return scope
