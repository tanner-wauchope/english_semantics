

class Expression:
    """
    Instances of this class construct literals from expression text.
    """
    def __init__(self, scope):
        self.scope = scope

    def __call__(self, expression_text):
        primitive_text = self.interpolate(expression_text)
        return eval(primitive_text)

    def interpolate(self, expression_text):
        raise NotImplementedError


class Text(Expression):
    """
    These expression are circumscribed in double quotes.
    Any text between brackets is compiled to python and evaluated.
    The evaluated text in reinserted into the containing expression.
    """
    pass


class Number(Expression):
    """
    These expressions are circumscribed in parentheses.
    Immediately before access, the expression is interpolated and evaluated.
    Any word prefixing an open parentheses is replaced with callable text.
    """
    pass
