
def regular_plural(singular):
    if singular.endswith('h'):
        return singular + 'es'
    elif singular.endswith('s'):
        return singular + 'es'
    elif singular.endswith('o') and singular[-2] not in 'aeiou':
        return singular + 'es'
    elif singular.endswith('y') and singular[-2] not in 'aeiou':
        return singular[:-1] + 'ies'
    return singular + 's'


def semi_regular_plural(singular):
    if singular.endswith('ma'):
        return singular + 'ta'
    elif singular.endswith('a'):
        return singular + 'e'
    elif singular.endswith('fe'):
        return singular[:-2] + 'ves'
    elif singular.endswith('f'):
        return singular[:-1] + 'ves'
    elif singular.endswith('um'):
        return singular[:-2] + 'a'
    elif singular.endswith('on'):
        return singular[:-2] + 'a'
    elif singular.endswith('o'):
        return singular + 'o'
    elif singular.endswith('is'):
        return singular[:-2] + 'es'
    elif singular.endswith('us'):
        return singular[:-2] + 'i'
    elif singular.endswith('x'):
        return singular[:-1] + 'ces'

