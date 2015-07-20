from plain_english.semantics import (
    predicate,
    determiners,
    expression,
    script,
)


def initialize(scope):
    scope['a'] = determiners.An(scope)
    scope['an'] = determiners.An(scope)
    scope['the'] = determiners.The(scope)
    scope['all'] = determiners.All(scope)
    scope['that'] = predicate.That()
    scope['nouns'] = {
        'Entity': predicate.OrderedSet('Entity', scope=scope),
        'Text': predicate.OrderedSet('Text', kind=expression.Text, scope=scope),
        'Number': predicate.OrderedSet('Number', kind=expression.Number, scope=scope),
        'Script': predicate.OrderedSet('Script', kind=script.Script, scope=scope)
    }
    return scope
