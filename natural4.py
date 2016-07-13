"""
the unit of composition is the _definition_
the head of a definition may be a sentence, but it may be a word too
"""


class Contradiction(Exception):
    pass


# TODO provide a default definition of __call__ that supports adjectives
# consider omitting underscore-prefixed names from unifies
# consider maintaining a list of of unifications that are filtered as the sentence is formed
class Word:
    definitions = {}

    def __init__(self, value):
        self.value = {value}
        self.name = ''
        self.specifier = Word()
        self.head = []
        self.complement = Word()
        self.properties = {}
        self.scope = None

    def __str__(self):
        return self.value or type(self).__name__

    def __hash__(self):
        return hash(str(self))

    def __getitem__(self, item):
        return self.properties[item]

    def __setitem__(self, key, value):
        self.properties[key] = value

    def __eq__(self, other):
        if self and other:
            return self.value == other.get_value
        elif not self and not other:
            return vars(self) == vars(other)

    def __call__(self, scope):
        self.scope = scope
        for definition in self.unifications():
            for line in definition:
                new = Scope(definition.scope.glob, self.properties)
                try:
                    evaluate(line, new)
                except Contradiction:
                    pass

    def unifies_with(self, other):
        if isinstance(self, type(other)):
            if self.value and other.get_value:
                return self.value == other.get_value
            elif not other.get_value:
                for key in other.specifier.properties:
                    mine, theirs = self.specifier[key], other.specifier[key]
                    if not mine.unifies_with(theirs):
                        return False
                for key in other.complement.properties:
                    mine, theirs = self.complement[key], other.complement[key]
                    if not mine.unifies_with(theirs):
                        return False
                return True

    def unifications(self):
        result = []
        for definition in type(self).definitions.values():
            if self.unifies_with(definition):
                result.append(definition)
        return result


# TODO figure out what calls the determiners
# maybe determiners will actually be like verbs?
class A(Word):
    def __call__(self, scope):
        name = self.complement.value.title()
        if name in scope:
            result = scope[name]
        else:
            result = type(self.complement, (Word,), {})()
            scope[name] = result
        return result


class The(Word):
    def __call__(self, scope):
        name = self.complement.value.lower()
        if name in scope:
            return scope[name]
        else:
            raise NameError(self.complement)


class Is(Word):
    def __call__(self, scope):
        subj, obj = self.subj, self.obj
        if obj and subj.is_.get(obj) in (None, obj):
            subj.is_[obj] = obj
        elif type(subj).is_.get(obj) in (None, obj):
            type(subj).is_[obj] = obj
        else:
            raise RuntimeWarning(self)


class Has(Word):
    def __call__(self, scope):
        subj, obj = self.subj, self.obj
        if subj:
            has_ = subj.has_
        else:
            has_ = type(subj).has_
        has_[obj] = has_.get(obj) or set()
        has_.add(obj)


class Scope:
    def __init__(self, glob=None, loc=None):
        self.glob = glob or {}
        self.loc = loc

    def __contains__(self, item):
        return self.loc and item in self.loc or item in self.glob

    def __getitem__(self, item):
        if self.loc and item in self.loc:
            return self.loc[item]
        else:
            return self.glob[item]

    def __setitem__(self, key, value):
        if self.loc is not None:
            self.loc[key] = value
        else:
            self.glob[key] = value

    def get(self, item):
        if item in self:
            return self[item]
        else:
            return Word(item)


def split(text, delimiters=' \t\n') -> list:
    """
    :param text: text that may contain the delimiters or quotes
    :param delimiters: tokens to be omitted if unquoted
    :return: the text split by unquoted delimiters
    """
    text += delimiters
    result = []
    segment = []
    state = 'unquoted'
    for char in text:
        if state == 'unquoted' and char == '"':
            state = 'quoted'
            segment.append(char)
            continue
        elif state == 'quoted' and char == '"':
            state = 'unquoted'
            segment.append(char)
            continue
        elif state == 'quoted' and char == '\\':
            state = 'escaped'
            continue
        elif state == 'escaped':
            state = 'quoted'
            segment.append(char)
            continue

        if not(char in delimiters and state == 'unquoted'):
            segment.append(char)
        elif segment:
            result.append(''.join(segment))
            segment = []

    if state == 'quoted':
        raise SyntaxError('Unclosed quotation: ' + ''.join(segment))
    return result


def merge(self, other):
    if self.specifies(other):
        other.specifier = self
    elif other.complements(self)
        self.complement = other
    else:
        self.head.append(other)


# TODO i need to initalize verbs somehow....
def evaluate(lexemes, scope):
    result = scope.get(lexemes[0])
    for lexeme in lexemes[1:]:
        try:
            result = merge(result, scope.get(lexeme))
        except Exception as e:
            return e
    return result


def interpret(line, scope):
    if line.startswith('\t'):
        scope['this'].append(line)
    elif not line.isspace():
        scope['this'] = evaluate(split(line))(scope)
    return scope['this']


# TODO maybe i can detect when the top function is missing args?
# I could gather args until the next blank line for those cases
def main() -> None:
    """ Spawn a Read-Eval-Print-Loop. """
    scope = Scope(dict(A=A, An=A, The=The, Is=Is, Has=Has))
    while True:
        print('???', end=' ')
        print(interpret(input(), scope))


if __name__ == '__main__':
    main()
