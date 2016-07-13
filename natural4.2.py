# TODO: create overrides for left_apply and right_apply
class Article:
    IS_KEYWORD = True
    SPECIFIES = Noun
    SPECIFIED_BY = None
    COMPLEMENTS = None
    COMPLEMENTED_BY = None


class Noun:
    IS_KEYWORD = False
    SPECIFIES = Verb
    SPECIFIED_BY = None
    COMPLEMENTS = None
    COMPLEMENTED_BY = Article


class Verb:
    IS_KEYWORD = False
    SPECIFIES = Preposition
    SPECIFIED_BY = Noun
    COMPLEMENTS = None
    COMPLEMENTED_BY = Noun


class Preposition:
    IS_KEYWORD = True
    SPECIFIES = None
    SPECIFIED_BY = Verb
    COMPLEMENTS = None
    COMPLEMENTED_BY = Noun


class Symbol:
    def merge(self, next):
        if type(next) is Word:
            raise TypeError(str(type(next)) + ' cannot follow a new symbol')
        else:
            return next.right_merge(self)


def leftward_cast(cls):
    for category in (cls.SPECIFIED_BY, cls.COMPLEMENTS):
        if not category.IS_KEYWORD:
            return category


def rightward_cast(cls):
    for category in (cls.COMPLEMENTED_BY, cls.SPECIFIES):
        if not category.IS_KEYWORD:
            return category


def cast(left, right):
    if type(left) is Symbol and type(right) is Symbol:
        raise TypeError("new symbols cannot be adjacent")
    elif type(left) is Symbol:
        left = leftward_cast(type(right))(left)
    elif type(right) is Symbol:
        right = rightward_cast(type(left))(right)
    return left, right


def merge(left, right, scope):
    left_is_head = (
        isinstance(right, left.COMPLEMENTED_BY) or
        isinstance(left, right.COMPLEMENTS)
    )
    right_is_head = (
        isinstance(right, left.SPECIFIES) or
        isinstance(left, right.SPECIFIED_BY)
    )
    if left_is_head:
        return left.right_apply(right, scope)
    elif right_is_head:
        return right.left_apply(left, scope)
    else:
        raise TypeError('Cannot merge: ' + str([left, right]))