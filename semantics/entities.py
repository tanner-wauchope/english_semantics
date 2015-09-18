import importlib
import collections

from plain_english.semantics import relations


class Entity:
    is_ = relations.Is('is_', {})
    has_ = relations.Relation('has_')

    def __init__(self):
        self.relations = collections.defaultdict(dict)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Primitive(Entity):
    """
    Wraps a primitive value that may be evaluted lazily from expression text.
    """
    def __init__(self, expression, scope):
        super().__init__()
        self.expression = expression
        self.value = None

    def format(self, scope):
        raise NotImplementedError


class Text(Primitive):
    """
    Constructs a text instance from text circumscribed in double quotes.
    Text between brackets is interpolated with named variables.
    """
    def format(self, scope):
        format_string = self.expression.replace('[', '{').replace(']', '}')
        return format_string.format(**scope)


class Number(Primitive):
    """
    Constructs a number instance from text circumscribed in parentheses.
    Contiguous alphabetic tokens are interpolated with named variables.
    """
    def format(self, scope):
        return eval(self.expression, scope)


class File(Primitive):
    """
    Constructs a file instance from a file path delimited by forward slashes.
    The semantics of Python paths is reused.
    """
    def format(self, scope):
        module_text = self.expression.replace('/', '.')
        return importlib.import_module(module_text, package=scope['__this__'])
