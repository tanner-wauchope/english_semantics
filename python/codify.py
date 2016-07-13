from plain_english.python import grammar


def phrases(tree, condition=(lambda x: isinstance(x, grammar.Noun))):
    result = []
    if hasattr(tree, 'specifier') and tree.specifier:
        result += phrases(tree.specifier, condition)
    if condition(tree):
        result.append(tree)
    if hasattr(tree, 'complement') and tree.complement:
        result += phrases(tree.complement, condition)
    return result


class Scope():
    def __init__(self) -> None:
        self._stack = [{}]

    def get(self, name):
        for frame in reversed(self._stack):
            if name in frame:
                return frame[name]

    def add(self, phrase):
        self._stack[-1][phrase.head] = phrase

    def push(self, *phrases):
        self._stack.append({})
        for phrase in phrases:
            self.add(phrase)

    def pop(self):
        return self._stack.pop()


def assignment(phrase, scope):
    # TODO: add support for plurals
    head = phrase.head
    if phrase.specifier and phrase.specifier.head in ('a', 'an'):
        return "{name} = noun('{kind}')".format(name=head.lower(), kind=head)
    elif not phrase.specifier and not scope.get(head):
        return "{name} = noun()".format(name=head.lower())


def clause(tree, scope):
    results = []
    for phrase in phrases(tree):
        line = assignment(phrase, scope)
        if line:
            results.append(line)
            scope.add(phrase)
    suffix = '()' if isinstance(tree, grammar.Verb) else ''
    return results + [tree.python() + suffix]


def sentence(clauses, scope):
    result = clause(clauses[0], scope)
    if len(clauses) > 1:
        extra = []
        for element in clauses[1:]:
            extra.extend(clause(element, scope))
        result.append(extra)
    return result


def paragraph(english, scope):
    tree = english[0][0]
    indefinites = [p for p in phrases(tree) if assignment(p, scope)]
    if all(child is None or child in indefinites for child in tree.children()):
        scope.push(*indefinites)
        result = [
            '@verb({types})'.format(
                types=', '.join("'" + c.head + "'" for c in tree.children()),
            ),
            'def {verb}({arguments}):'.format(
                verb=tree.head,
                arguments=', '.join(c.head.lower() for c in tree.children())
            )
        ]
        if len(english) > 1:
            extra = []
            for element in english[1:]:
                extra.extend(sentence(element, scope))
            result.append(extra)
        scope.pop()
        return result
    return [sentence(s, scope) for s in english]


def flatten(element, indent='') -> list:
    """
    :param list element: a paragraph, a sentence, or a clause
    :return: indented python that represents the english
    """
    lines = []
    for part in element:
        if isinstance(part, str):
            lines.append(indent + part)
        else:
            lines.extend(flatten(part, indent=indent + '\t'))
    return lines


def codify(block):
    return '\n'.join(flatten(paragraph(block, scope=Scope())))