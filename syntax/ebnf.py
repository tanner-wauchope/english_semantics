"""
This is a work in progress. It is not yet used for parsing.

This is the grammar for the supported subset of English.
The specification language is an adaptation of Extended Backus Naur Form.
Tuples behave like comma-separated expressions in EBNF. They are immutable.
Lists behave like pipe-separated expressions in EBNF. They are mutable
Sets of either strings or regular expressions are the terminal expressions.
By convention, additions to lists preserve the original type signature.
"""
import re

# Python numbers and strings
primitive = {
    # based on docs.python.org/3/library/re.html#simulating-scanf
    re.compile(r'[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?'),
    # based on stackoverflow.com/questions/249791
    re.compile(r'''("(?:[^"\\]|\\.)*")|('(?:[^'\\]|\\.)*')'''),
}

# extensible noun modification
noun_specifier = [{'the'}]
noun_specifier_singular = [noun_specifier, {'a', 'an'}]
noun_specifier_plural = [noun_specifier, {''}]
noun_complement = [primitive]
noun_complement_singular = [noun_complement]
noun_complement_plural = [noun_complement]

# open word classes
singular_noun = set()
plural_noun = set()
singular_verb = {'is'}
plural_verb = {'are'}
base_verb = [{'be'}, plural_verb]

# simple noun phrases
singular_noun_phrase = [(noun_specifier_singular, singular_noun, noun_complement_singular)]
plural_noun_phrase = [(noun_specifier_plural, plural_noun, noun_complement_plural)]
noun_phrase = [primitive, singular_noun_phrase, plural_noun_phrase]

# simple statements
verb_complement = (
    ['', noun_phrase],
    ['', ('to', noun_phrase)],
    ['', ('for', noun_phrase)],
)
singular_predicate = [singular_verb, verb_complement]
plural_predicate = [plural_verb, verb_complement]
statement = [
    (singular_noun_phrase, singular_predicate),
    (plural_noun_phrase, plural_predicate),
]

# coordinating conjunctions
coordinator = {'and', 'or'}
plural_noun_phrase.append((noun_phrase, coordinator, noun_phrase))
singular_predicate.append((singular_predicate, coordinator, singular_predicate))
plural_predicate.append((plural_predicate, coordinator, plural_predicate))

# possession and noun prepositions
singular_verb.add('has')
plural_verb.add('have')
noun_complement.append(['', ({'of', 'in', 'on'}, noun_phrase)])
noun_specifier.append((noun_phrase, {"'s", "'"}))

# introductory phrases for pattern matching
subject_match = 'for', noun_phrase
direct_object_match = ['', subject_match], 'to', base_verb, ['', noun_phrase]
indirect_object_match = ['', direct_object_match], 'to', noun_phrase
line = [statement, [
    subject_match,
    direct_object_match,
    indirect_object_match,
    (indirect_object_match, subject_match),
]]

# relative clauses
noun_complement_singular.append(('that', singular_verb, verb_complement))
noun_complement_plural.append(('that', plural_verb, verb_complement))
noun_complement.append((['', 'that'], [
    (singular_noun_phrase, singular_verb),
    (singular_noun_phrase, plural_verb),
]))

# input and output
singular_noun_phrase.append(([], {'I', 'you'}, []))
singular_verb.add('say')
plural_verb.add('say')
