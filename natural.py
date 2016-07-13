
class Noun:
    is_ = set()
    has_ = set()

    def __init__(self, value):
        self.value = value
        self.is_ = {}
        self.has_ = {}

    def __str__(self):
        return self.value or type(self).__name__

    def __hash__(self):
        return hash(str(self))


def a(token, scope):
    if isinstance(token, str):
        result = type(token, (Noun,), {})()
        scope[token] = result
    else:
        result = token
    return result


def the(token, scope):
    if token.lower() in scope:
        return scope[token.lower()]
    else:
        raise NameError(token)



class Verb:
    name = ''
    scope = {}
    body = []

    def __init__(self, subj, obj):
        self.subj = subj
        self.obj = obj

    def __call__(self):
        for consequence in type(self).body:
            global_scope = type(consequence).scope
            local_scope = {
                self.subj.name: self.subj,
                self.obj.name: self.obj,
            }
            exec(consequence.name + '()', global_scope, local_scope)
        return self


class Is(Verb):
    def __call__(self):
        subj, obj = self.subj, self.obj
        if obj and subj.is_.get(obj) in (None, obj):
            subj.is_[obj] = obj
        elif type(subj).is_.get(obj) in (None, obj):
            type(subj).is_[obj] = obj
        else:
            raise RuntimeWarning(self)


class Has(Verb):
    def __call__(self):
        subj, obj = self.subj, self.obj
        if subj:
            has_ = subj.has_
        else:
            has_ = type(subj).has_
        has_[obj] = has_.get(obj) or set()
        has_.add(obj)


class Do(Verb):
    def __call__(self):
        exec(repr(self.obj), {})


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


def evaluate(line, scope):
    new = None
    verb = None
    lexemes = split(line)
    for lexeme in lexemes:
        token = scope.get(lexeme.title())

        if not token and not lexeme.startswith('`'):
            if new:
                raise NameError(lexeme)
            else:
                new = lexeme

        if isinstance(token, Verb):
            if verb:
                raise SyntaxError(verb)
            else:
                verb = token

    if new:
        if verb:
            noun = Noun(new)
            scope[new] = noun
        else:
            verb = type(new, (Verb,), {})
            scope[new] = verb

    try:
        center = lexemes.index(verb)
    except:
        center = 0

    subj = obj = lambda x: x
    for i, lexeme in enumerate(lexemes):
        token = scope[lexeme.title()]
        if i < center:
            subj = subj(token)
        elif i > center:
            obj = obj(token)

    if verb:
        return verb(subj, obj)
    else:
        return obj


def main(scope) -> None:
    """ Spawn a Read-Eval-Print-Loop using 'scope' as the global scope. """
    scope.update(A=a, An=a, The=the, Is=Is, Has=Has, Do=Do)
    while True:
        print('???', end=' ')
        line = input()
        try:
            result = evaluate(line, scope)
        except (SyntaxError, NameError) as e:
            print(e)
            continue

        while not line.isspace():
            print('...', end=' ')
            line = input()
            result.append(line)
        print(result)


if __name__ == '__main__':
    main({})
