"""
the unit of composition is the _definition_
the head of a definition may be a sentence, but it may be a word too
"""
import functools


class Contradiction(Exception):
    pass


# TODO provide a default definition of __call__ that supports adjectives
# consider omitting underscore-prefixed names from __lt__
# consider maintaining a list of of unifications that are filtered as the sentence is formed
@functools.total_ordering
class Word:
    def __init__(self, value, scope):
        self.value = {value}
        self.name = ''
        self.scope = scope
        self.specifiers = []
        self.head = []
        self.complements = []

    def __str__(self):
        return self.value or type(self).__name__

    def __hash__(self):
        return hash(str(self))

    def __getitem__(self, item):
        return vars(self)[item]

    def __setitem__(self, key, value):
        vars(self)[key] = value

    def __mul__(self, other):
        self.complements.append(other)
        if self._unifications():
            return self
        else:
            self.complements.pop()
            return self.__rmul__(other)

    def __rmul__(self, other):
        other.specifiers.append(self)
        if other.unifications():
            return other
        else:
            other.specifiers.pop()
            raise SyntaxError(str(self) + ' does not combine with ' + str(other))

    def __eq__(self, other):
        if self and other:
            return self.value == other.get_value
        elif not self and not other:
            return vars(self) == vars(other)

    def __lt__(self, other):
        if self and other:
            return self.value < other.get_value
        elif isinstance(self, type(other)):
            for key in vars(other):
                mine, theirs = self[key], other[key]
                if not (mine < theirs):
                    return False
            return True

    def __bool__(self):
        return self.value

    def _unifications(self):
        result = []
        for definition in vars(type(self)):
            if self < definition:
                result.append(definition)
        return result

    def __call__(self, scope):
        for definition in self._unifications():
            try:
                for line in definition:
                    scope = Scope(definition.scope.glob, vars(self))
                    tokens = evaluate(line, scope)
                    apply(tokens, scope)
            except Contradiction:
                pass
        return self


class A(Word):
    def __call__(self, token, scope):
        name = token.get_value.title()
        if name in scope:
            result = scope[name]
        else:
            result = type(token, (Word,), {})()
            scope[name] = result
        return result


class The(Word):
    def __call__(self, token, scope):
        name = token.get_value.lower()
        if name in scope:
            return scope[name]
        else:
            raise NameError(token)

# TODO fix the verb defintions
class Is(Word):
    def prove(self):
        subj, obj = self.subj, self.obj
        if obj and subj.is_.get(obj) in (None, obj):
            subj.is_[obj] = obj
        elif type(subj).is_.get(obj) in (None, obj):
            type(subj).is_[obj] = obj
        else:
            raise RuntimeWarning(self)


class Has(Word):
    def prove(self):
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


def evaluate(lexemes, scope):
    tokens = []
    for lexeme in lexemes:
        if lexeme in scope:
            return scope[lexeme]
        else:
            token = Word(lexeme, scope)
        tokens.append(token)
    return tokens


def apply(tokens, scope):
    """ chain-compose -> unify -> search """
    composition = lambda result, scope: result
    for token in tokens:
        composition = composition(token, scope)
    return composition.prove()


# TODO: consider evaluating body lines too; maybe should consolidate with first line processing
def main() -> None:
    """ Spawn a Read-Eval-Print-Loop. """
    scope = Scope(dict(A=A, An=A, The=The, Is=Is, Has=Has))
    while True:
        print('???', end=' ')
        line = input()
        try:
            tokens = evaluate(split(line), scope)
        except Exception as e:
            print(e)
            continue

        body = []
        while not line.isspace():
            print('...', end=' ')
            line = input()
            body.append(split(line))

        try:
            head = apply(tokens, scope)
            vars(type(head))[head] = body
            print(head)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
