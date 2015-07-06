
"""
I need to eventually add desugaring to the syntax module.
The desugaring will remove inflections (plurals and possessives).
"""

def pluralize(singular):
    if singular.endswith('h'):
        return singular + 'es'
    elif singular.endswith('s'):
        return singular + 'es'
    elif singular.endswith('o') and singular[-2] not in 'aeiou':
        return singular + 'es'
    elif singular.endswith('y') and singular[-2] not in 'aeiou':
        return singular[:-1] + 'ies'
    return singular + 's'