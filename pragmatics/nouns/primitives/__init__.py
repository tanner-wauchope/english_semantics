
class CannotModifyPrimitive(Exception):
    pass


class Primitive:
    def is_(self, subject, predicate):
        raise CannotModifyPrimitive

    def has_(self, subject, predicate):
        raise CannotModifyPrimitive
