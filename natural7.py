import itertools


def predicate(parts):
    facts = set()
    for i, part in enumerate(parts):
        for entity in part:
            if hasattr(entity, '__dict__'):
                facts &= vars(entity)[i]

    matches = []
    for fact in facts:
        if unifies(fact, parts):
            matches.append(fact)

    for i, part in enumerate(parts):
        if not part:
            value = ()
            for match in matches:
                value += (match[i],)
            parts = parts[:i] + (value,) + parts[i + 1:]

    for fact in itertools.product(parts):
        for i, entity in enumerate(fact):
            if hasattr(entity, '__dict__'):
                entity[i] = entity.get(i, set())
                entity[i].add(fact)


def unifies(items, rule):
    if len(items) != len(rule):
        return False
    for item, kind in zip(items, rule):
        # TODO improve by looping over entities in item and entities in kind
        if not isinstance(item, type(kind)):
            return False
        elif hasattr(item, '__dict__') and hasattr(kind, '__dict__'):
            # TODO improve by handling derived properties
            for relation in vars(item).items():
                if relation not in vars(kind).items():
                    return False
        elif item != kind:
            return False
    return True


def parse(items, grammar):
    for start in range(len(items)):
        for rule in reversed(grammar):
            stop = start + len(rule) - 1
            prefix, stem, suffix = items[:start], items[start:stop], items[stop:]
            if unifies(stem, rule):
                return parse(prefix + (rule[-1](stem),) + suffix)
    return items


def define(items, grammar):
    signature, new_meaning = items[:-1], items[-1]
    old_meaning = grammar.get(signature, predicate)
    def new(parts):
        old_meaning(parts)
        new_meaning()
    grammar[signature] = new


def evaluate(line):
    # call split, parse, and apply
    raise NotImplementedError