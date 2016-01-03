import code

from plain_english.python import scan, tokenize, parse, codify, register


def interpret(english):
    """
    :param english: English text to be interpreted
    :return: a python tree or list of python trees if the English is valid
             an Exception object if the English was invalid
    """
    try:
        lexemes = scan.scan(english)
        tokens = tokenize.tokenize(lexemes)
        trees = parse.parse(tokens)
        return codify.codify(trees)
    except Exception as e:
        return e


def compile_command(english, filename='', symbol='exec'):
    last = english[-1].split('\n')[-1]
    if not last.strip() or last == last.lstrip():
        interpretation = interpret(english)
        if type(interpretation) in (SyntaxError, ValueError, OverflowError):
            raise SyntaxError
        elif isinstance(interpretation, Exception):
            raise SyntaxError(str(interpretation))
        else:
            return compile(interpretation, filename, symbol)


def run_interpreter():
    noun, verb, _ = register.register()
    default_scope = {
        'noun': noun,
        'verb': verb,
        '_': _,
    }
    interpreter = code.InteractiveConsole(locals=default_scope)
    interpreter.compile = compile_command
    interpreter.interact(banner='Plain English v0.1')


class Discourse:
    """
    Keeps track of lines that have not yet formed a complete paragraph
    """
    def __init__(self):
        """
        Initialize a buffer to hold lines of an incomplete paragraph.
        """
        self.paragraph = ''

    def interpret(self, line):
        """
        If the line completes a paragraph, parse it and reset it.
        """
        if self.paragraph and not line.startswith('\t'):
            interpretation = interpret(self.paragraph)
            self.paragraph = line + '\n'
            return interpretation
        else:
            self.paragraph += line + '\n'
