# import sys
# import io

from plain_english.semantics.initialize import initialize
from plain_english.semantics.entities import Entity, Text

"""
A writer should not ordinarily have to wrap any previous defined words in quotes.
Wrapping something in quotes should cause a definition to be *replaced*.
By contrast, topic sentences that don't wrap words in quotes *extend* a pattern's implications.

A topic sentence should only be eagerly evaluated if it contains a definite noun phrase:
    - prints statements contain "you"
    - input statements contain "I"
    - statements that read or write a file contain a file literal

If this was so, constructors and properties might look like this:

    an "X" is a Y. # nothing is instantiated. this is presupposed by typed noun phrases.
    the X has a Z. # a Z is instantiated when the previous sentence is matched.

    an X has a "W". # nothing is instantiated. this is presupposed by "'s".
    the X ... # this happens when the previous sentence is matched.

"""


def test_noun_definition():
    scope = initialize({})
    a = scope['a']
    an = scope['an']
    superclass_set = an.Entity
    a._Dog_.is_(superclass_set)('a.Dog.has_(a.Dog)')
    dog_class = scope['singular']['Dog'].kind
    assert dog_class is not Entity
    assert issubclass(dog_class, Entity)
    definition = dog_class.is_.definitions[0]
    assert definition.complement == superclass_set
    assert definition.support_text == 'a.Dog.has_(a.Dog)'


def test_noun_instantiation():
    scope = initialize({})
    a = scope['a']
    an = scope['an']
    the = scope['the']
    a._Dog_.has_(an.Entity)('a.Dog.has_(a.Dog)')
    dog_class = scope['singular']['Dog'].kind
    scope['singular']['Dog'].members.append(dog_class())
    a.Dog.has_(the.Dog)()
    assert len(scope['singular']['Dog'].members) is 2
    assert scope['singular']['Dog'].members[0] is not scope['singular']['Dog'].members[1]


def test_verb_definition():
    scope = initialize({})
    an = scope['an']
    ordered_set = an.Entity
    ordered_set._loves_("the.Entity.has_(the.Text('Love'))")
    for key, value in ordered_set.kind.__dict__.items():
        print('key: ' + str(key))
        print('value: ' + str(value))
    definition = ordered_set.kind.loves_.definitions[0]
    assert definition.subject.name == 'Entity'
    assert definition.subject.kind is Entity
    assert definition.complement is None
    assert definition.support_text == "the.Entity.has_(the.Text('Love'))"


def test_verb_execution():
    scope = initialize({})
    an = scope['an']
    the = scope['the']
    an.Entity._loves_("the.Entity.has_(the.Text('Love'))")

    first_ordered_set = an.Entity
    first_ordered_set.has_(the.Text('Love'))()
    entity = first_ordered_set.members[0]
    assert 'Love' in entity.relations['has_'][Text].members

    ordered_set = an.Entity
    ordered_set.instantiate()
    ordered_set.loves_()
    entity = ordered_set.members[0]
    assert 'Love' in entity.relations['has_'][Text].members




# TODO: Need to implement 'say' and verb inflections
# def test_verb_execution():
#     scope = initialize({})
#     an = scope['an']
#     entity = an.Entity
#     entity._greets_()("the.Entity.says('Hello')")
#     saved_stdout = sys.stdout
#     out = io.StringIO()
#     try:
#         sys.stdout = out
#         an.Entity.greets()
#         assert out.getvalue() == 'Hello'
#     finally:
#         sys.stdout = saved_stdout