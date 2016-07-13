from plain_english.natural5 import *


def tanner_semantics():
    # tanner is a person
    tanner = Word('tanner')
    Person = type('Person', (Noun,), {})
    person = Person()
    executable = Is(tanner, person)
    scope = {}
    executable.run(scope)
    assert scope['tanner'] is person



def student_semantics():
    # student is an occupation

    # the occupation has a salary
    # the salary is 0
    # Tanner has the occupation

    # programmer is an occupation
    # the occupation has a salary
    # the salary is 1
    # Tanner has the occupation

    # QA is an occupation
    # the occupation has a salary
    # the salary is 1

    # Tanner has occupations
    # the occupations # student, programmer

    # a person loves an occupation
    #   the person has the occupation
    #   the occupation has a salary
    #   the salary is 1

    # Tanner loves an occupation
    # the occupation # programmer
    assert False


def tanner_syntax():
    tanner = Word('tanner')
    Person = type('Person', (Noun,), {})
    person = Person()
    executable = Is(tanner, person)
    assert executable == parse("Tanner is a person")




