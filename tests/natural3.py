import io
import sys

import pytest

from plain_english.natural6 import *


def test_phrase():
    scope = {}
    signature = (object, 'Has', object)
    Has = type('Has', (Phrase,), {'signatures': [signature]})

    # add a relationship to scope
    subj = Phrase()
    obj = Phrase()
    predicate = Has(subj, Has, obj)
    assert not predicate.satisfied(scope)
    predicate.invoke(scope)
    relation = Has(subj, Has, obj)
    assert relation in Has.relations
    assert relation in vars(subj)[Has]
    assert predicate.satisfied(scope)

    # query for subj and obj
    predicate = Has('x', Has, 'y')
    assert not predicate.satisfied(scope)
    predicate.invoke(scope)
    assert scope['x'] == subj
    assert scope['y'] == obj
    assert predicate.satisfied(scope)

    # query for subj only
    predicate = Has('z', Has, obj)
    assert not predicate.satisfied(scope)
    predicate.invoke(scope)
    assert scope['z'] == subj
    assert predicate.satisfied(scope)


def test_assignment():
    scope = {
        'x': 1,
        'y': 2,
    }
    assignment = Assignment('x', Assignment, 'y')
    assert not assignment.satisfied(scope)
    assignment.invoke(scope)
    assert scope['x'] == scope['y']
    assert assignment.satisfied(scope)


def test_indefinite_article():
    scope = {}
    thing = Instantiation('a', 'thing').invoke(scope)
    assert type(scope['thing']).__name__ == 'Thing'
    assert scope['thing'] == thing


def test_definite_article():
    scope = {}

    # fail for unexpected arguments
    with pytest.raises(NameError):
        Lookup('the', 'thing').invoke(scope)
    with pytest.raises(TypeError):
        Lookup('the', 2).invoke(scope)

    # return any object found in scope
    noun = Phrase()
    assert Lookup('the', noun).invoke(scope) is noun


def test_noun_build_phrases():
    scope = {}


    noun_phrase = next(build_noun_phrases(['a', 'thing'], scope))
    assert type(noun_phrase) == Instantiation

    noun_phrase = next(build_noun_phrases(['the', Phrase()], scope))
    assert type(noun_phrase) == Lookup


# def test_parse():
    # parts = ['a', 'thing']
    # match, remainder = parse(parts, [Instantiation])
    # assert len(match) == 1
    # assert len(remainder) == 0
    # phrase = match[0]
    # assert isinstance(phrase, Instantiation)
    # assert phrase.parts == parts
    #
    # parts = ['the', Phrase()]
    # match, remainder = parse(parts, [Lookup])
    # assert len(match) == 1
    # assert len(remainder) == 0
    # phrase = match[0]
    # assert isinstance(phrase, Lookup)
    # assert phrase.parts == parts
    #
    # parts = [Phrase('x'), 'is', Phrase('y')]
    # match, remainder = parse(parts, [Assignment])
    # assert len(match) == 1
    # assert len(remainder) == 0
    # phrase = match[0]
    # assert isinstance(phrase, Phrase)
    # assert phrase.parts == parts

    # parts = ['the', Phrase('x'), 'is', 'a', Phrase('y')]
    # match, remainder = parse(parts, [Assignment])
    # assert len(match) == 1
    # assert len(remainder) == 0
    # phrase = match[0]
    # assert isinstance(phrase, Phrase)
    # subj, verb, obj = phrase.parts
    # assert subj.parts + [verb] + obj.parts == parts


def test_match():
    signature = (object, str, object)

    # 1 or fewer strings
    assert match([Phrase(), Phrase(), Phrase()], signature) is None
    assert match([Phrase(), Phrase(), str()], signature) is None
    assert match([Phrase(), str(), Phrase()], signature) == (object, str, object)
    assert match([str(), Phrase(), Phrase()], signature) is None

    # 2 or more strings
    assert match([Phrase(), str(), str()], signature) == (object, str, object)
    assert match([str(), Phrase(), str()], signature) is None
    assert match([str(), str(), Phrase()], signature) == (object, str, object)
    assert match([str(), str(), str()], signature) == (object, str, object)


def test_get_signature():
    new  = get_signature(['x', '"has"', 'y'], {})
    assert new == [object, 'has', object]


def test_build_clause():
    scope = {'x': 1, 'y': 2, Assignment: [[object, 'is', object]]}
    clause = build_clause(['x', 'is', 'y'], scope)
    assert not clause.satisfied(scope)
    clause.invoke(scope)
    assert scope['x'] == 2
    assert clause.satisfied(scope)


def test_split():
    def matches(generator, li):
        return list(generator) == li

    # single lexemes
    assert matches(split('"\n"', '\n'), ['"\n"'])
    assert matches(split('ab', '\n'), ['ab'])

    # delimiter as prefix or suffix
    assert matches(split('\n"\n"', '\n'), ['"\n"'])
    assert matches(split('"\n"\n', '\n'), ['"\n"'])
    assert matches(split('\nab', '\n'), ['ab'])
    assert matches(split('ab\n', '\n'), ['ab'])

    # split quote and non-quote lexemes
    assert matches(split('ab\ncd', '\n'), ['ab', 'cd'])
    assert matches(split('"\n"\n"\n"', '\n'), ['"\n"', '"\n"'])
    assert matches(split('ab\n"\n"', '\n'), ['ab', '"\n"'])
    assert matches(split('"\n"\nab', '\n'), ['"\n"', 'ab'])

    # handle multiple occurrences of the delimiter
    assert matches(split('ab\n\ncd', '\n'), ['ab', 'cd'])

    # handle multiple delimiters
    assert matches(split('ab \n cd', '\n '), ['ab', 'cd'])

    # split a quotation ending with an escaped backslash
    assert matches(split(r'"\\"', '\n'), [r'"\"'])

    # split string that whose ending quote is escaped
    with pytest.raises(SyntaxError):
        list(split('"\\"', '\n'))


def test_evaluate():
    scope = {Assignment: Assignment.signatures}
    evaluate("x is a thing", scope)
    assert type(scope['x']).__name__ == 'Thing'


def test_interpret():
    stdin = sys.stdin
    stdout = sys.stdout


    # test non-exceptional input
    sys.stdin = io.StringIO(
        "x is a thing\n"
        'x\n'
        'exit\n'
    )
    sys.stdout = io.StringIO()
    interpret()
    output = sys.stdout.getvalue()
    assert output.startswith('> > <')
    assert 'Thing' in output
    assert output.endswith('\n> ')

    # test exceptional input
    sys.stdin = io.StringIO(
        "garbage\n"
        "exit\n"
    )
    sys.stdout = io.StringIO()
    interpret()
    output = sys.stdout.getvalue()
    assert output.startswith("> Traceback")

    sys.stdin = stdin
    sys.stdout = stdout

