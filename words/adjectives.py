import decimal

def handle_atom(atom):
    try:
        return decimal.Decimal(atom)
    except ValueError:
        return eval(atom)
    except NameError:
        return atom

class Adjective:
    pass