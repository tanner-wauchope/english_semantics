from keyword import iskeyword


def head(tree):
    """
    :param tree: a syntax tree
    :return: the tree's head, except:
             any python keyword is disambiguated with a trailing underscore
             any leading single quote is removed
             any trailing single quote is replaced with an underscore
             any leading double quote is replaced with a single quote
             any trailing double quote is replaced with a single quote
    """
    result = tree.head
    if iskeyword(result):
        result += '_'
    if result.startswith("'"):
        result = result[1:]
    if result.endswith("'"):
        result = result[:-1] + '_'
    if result.startswith('"'):
        result = "'" + result[1:]
    if result.endswith('"'):
        result = result[:-1] + "'"
    return result

def subordinate(tree):
    """
    :param tree: a syntax tree
    :return: python whose execution tree mimics the abstract syntax tree
    """
    result = ''
    if tree.specifier:
        result += subordinate(tree.specifier) + '.'
    result += head(tree)
    if tree.complement:
        result += '(' + subordinate(tree.complement) + ')'
    return result


def coordinate(elements, indent, quote_mark):
    """
    :param elements: a list of speech elements
    :param indent: the indentation of each line of python after the first
    :quote_mark: the quotation marks used to make the coordination lazy
    :return: lazy python that coordinates the elements
    """
    if elements:
        conjoins = []
        for element in elements:
            conjoins.append(quote_mark + codify(element) + quote_mark)
        return '(\n' + indent + (',\n' + indent).join(conjoins) + ')'
    return ''


def codify(english):
    """
    :param english: a paragraph, a sentence, or a clause
    :return: python that represents the english
    """
    if isinstance(english, list) and isinstance(english[0], list):
        return codify(english[0]) + coordinate(english[1:], '\t', "'''") + '\n'
    elif isinstance(english, list):
        return subordinate(english[0]) + coordinate(english[1:], '\t\t', '"')
    return subordinate(english)