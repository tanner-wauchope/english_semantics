from plain_english.python.register import (
    register,
    Verb,
    distribute,
    matches,
    compatible,
    Noun,
)


def test_compatible():
    entity1 = Noun()
    entity1.properties['x'] = 1
    entity2 = Noun()
    entity2.properties['x'] = 2
    entity3 = Noun()
    entity3.entities = [entity1, entity2]
    assert compatible(entity1, entity1) == entity1
    assert compatible(entity2, entity2) == entity2
    assert compatible(entity3, entity3) == entity3
    assert compatible(entity1, entity2) is None
    assert compatible(entity1, entity3) is None
    assert compatible(entity2, entity3) is None


def test_matches():
    entity1 = Noun()
    entity2 = Noun()
    entity1.entities = [entity2]
    entities = entity1, entity2

    def function(subject, complement):
        pass

    function.kinds = entities
    result = matches(function, entities)
    print(result[1].__dict__)
    print(entity2.__dict__)
    print(result[1] == entity2)
    assert result == [[entity1], entity2]


def test_distribute():
    entity1 = Noun(properties={'value': 1})
    entity2 = Noun(properties={'value': 2})
    entities = Noun(properties={'value': 3}, entities=[entity1, entity2])

    def increment(subject, complement):
        subject.properties['value'] += complement.properties['value']

    distribute(increment, [entity1, entity2])
    assert entity1.properties['value'] == 3
    distribute(increment, [entity1, [entities]])
    assert entity1.properties['value'] == 6
    distribute(increment, [entity1, entities])
    assert entity1.properties['value'] == 14


class TestVerb:
    def test_call(self):

        def append(*args):
            print(args[0])
            print(args[1])
            args[0].entities.append(args[1])
            print(args[0].entities)

        append.kinds = (Noun(), Noun())
        verb = Verb()
        verb.functions.append(append)
        entity1 = Noun()
        entity2 = Noun()
        verb(entity1, entity2)
        assert entity1 == Noun(entities=[entity2])


def test_register_noun():
    noun, verb = register()
    entity = noun()
    assert isinstance(entity, Noun)
    dog1 = noun('Dog')
    assert isinstance(dog1, Noun)
    assert type(entity) != type(dog1)
    dog2 = noun('Dog')
    assert dog1 == dog2
    assert dog1 is not dog2
    assert type(dog1) == type(dog2)


def test_register_verb():
    noun, verb = register()

    @verb('Noun', int)
    def has(subject, complement):
        pass

    assert has.functions[0].kinds == ('Noun', int)

    @verb('Noun', str)
    def has(subject, complement):
        pass

    assert has.functions[1].kinds == ('Noun', str)


def test_register_thread_safety():
    noun1, verb1 = register()
    noun2, verb2 = register()
    dog1 = noun1('Dog')
    dog2 = noun2('Dog')
    assert type(dog1) is not type(dog2)

    @verb1('Noun', int)
    def has(subject, complement):
        pass

    has1 = has

    @verb2('Noun', int)
    def has(subject, complement):
        pass

    assert has1 is not has



# def test_verb_execution():
#     noun, verb = register()
#
#     entity = noun()
#     entity.has(1)
#     assert entity.properties['has'] == 1

#
# def test_verb_execution():
#     scope = initialize({})
#     an = scope['an']
#     the = scope['the']
#     an.Entity._loves_("the.Entity.has_(the.Text('Love'))()")
#
#     first_ordered_set = an.Entity
#     first_ordered_set.has_(the.Text('Love'))()
#     entity = first_ordered_set.members[0]
#     assert 'Love' in entity.relations['has_'][Text].members
#
#     ordered_set = an.Entity
#     ordered_set.instantiate()
#     ordered_set.loves_()
#     entity = ordered_set.members[0]
#     assert 'Love' in entity.relations['has_'][Text].members
