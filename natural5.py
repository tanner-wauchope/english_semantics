"""
the unit of composition is the _definition_
the head of a definition may be a sentence, but it may be a word too
"""


class Contradiction(Exception):
    pass


class Noun:
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


class A(Word):
    def apply(self, scope):
        name = self.complement.value.title()
        if name in scope:
            result = scope[name]
        else:
            result = type(self.complement, (Word,), {})()
            scope[name] = result
        return result


class The(Word):
    def apply(self, scope):
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


def split_lines(buffer):
    try:
        block = ''.join(buffer)
        return split(block, delimiters='\n.:')
    except SyntaxError:
        return None


def tokenize(lexemes, scope):
    tokens = []
    for lexeme in lexemes:
        if lexeme in scope:
            token = scope[lexeme]
        elif lexeme.startswith('"'):
            token = lexeme
        elif lexeme.isalpha():
            token = Word(lexeme)
        else:
            raise NameError(lexeme)
        tokens.append(token)
    return tokens


def parse():
    pass


def apply_articles(tokens, scope):
    results = []
    article = None
    for token in tokens:
        if token in (A, The):
            article = token
        elif article:
            # TODO: indefinte article should make classes only if scope.loc is None
            # this should protect against typos in a principled way
            results.append(article.apply(token))
            article = None
        else:
            results.append(token)
    return results


class Verb:
    def __init__(self, tokens, verb_index):
        self.subject = tokens[:verb_index]
        self.complement = tokens[verb_index + 1:]


def get_verb(tokens, scope):
    new_tokens = []
    for i, token in enumerate(tokens):
        if issubclass(token, Verb):
            return token(tokens, i)
        elif isinstance(token, Word):
            new_tokens.append((i, token))

    if len(new_tokens) == 1 and not scope.loc:
        i, token = new_tokens[0]
        return type(token.name, (Verb,), {})(tokens, i)

    raise SyntaxError("Cannot identify or define verb")


def evaluate(lines, scope):
    if len(lines) > 1:
        scope['This'].append(lines)
        return ''

    lexemes = split(lines[0], ' ')
    tokens = tokenize(lexemes, scope)
    tokens = apply_articles(tokens, scope)
    executable = get_verb(tokens, scope)
    if executable.definite():
        try:
            scope['This'] = executable.run()
            return ''
        except Exception as e:
            return e


def interpret() -> None:
    """ Spawn a Read-Eval-Print-Loop. """
    scope = Scope(dict(A=A, An=A, The=The, Is=Is, Has=Has, This=[]))
    buffer = []
    while True:
        print('???', end=' ')
        inp = input() + '\n'
        buffer.append(inp)
        if inp.isspace() or not inp.startswith('\t'):
            lines = split_lines(buffer)
            if lines:
                print(evaluate(lines, scope))
                buffer = []


if __name__ == '__main__':
    interpret()
