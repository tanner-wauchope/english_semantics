import language.syntax as syntax
from language.syntax.primitives import number, quote, possessive, topic


class Token:
    """
    A token pairs a lexeme and a word class.
    This class intermediates between constituencies and word classes.
    If the word class of a token is updated,
        the behavior of any constituencies that use that token will update.
    """
    def __init__(self, lexeme, word_class):
        """
        Save the lexeme and the initial word class.
        """
        self.lexeme = lexeme
        self.word_class = word_class


def match(lexeme):
    """
    :param lexeme: a lexeme that is possibly punctuated or numeric
    :return: whether the lexeme is a number, quote, possessive, or variable
    """
    if number.match(lexeme):
        return number.Number
    elif quote.match(lexeme):
        return quote.Quote
    elif possessive.match(lexeme):
        return possessive.Possessive
    elif topic.match(lexeme):
        return topic.Topic


def define(lexeme, word_class, subtopics):
    """
    Create a token and save new subtopics.
    :param lexeme: a token that is possibly a subtopic
    :param subtopics: map of variables in this paragraph to subtopics
    :return: a token with the specified lexeme and word class
    """
    token = Token(lexeme, word_class)
    if word_class is topic.Topic:
        subtopics[lexeme.strip("'")] = token
    return token


def lookup(lexeme, subtopics, topics):
    """
    :param lexeme: an non-punctuated, non-numeric lexeme
    :param subtopics: map of variables in this paragraph to word classes
    :param topics: map of variables in previous paragraphs to word classes
    :return: a word class
    """
    name = lexeme.lower()
    if name in subtopics:
        return subtopics[name]
    elif name in topics:
        return topics[name].word_class
    elif hasattr(syntax, name + '_'):
        return getattr(syntax, name + '_')
    raise NameError(name + ' must be alphabetical.')


def tokenize(paragraph, topics):
    """
    Replaces the lexemes in the paragraph with tokens.
    :param paragraph: sentences that contain lines that contain lexemes
    :param topics: map of variables to previously discussed topics
    :return: sentences that contain lines that contain tokens
    """
    subtopics = {}
    result = []
    for sentence in paragraph:
        result.append([])
        for line in sentence:
            result[-1].append([])
            for lexeme in line:
                word_class = match(lexeme)
                if word_class:
                    token = define(lexeme, subtopics)
                else:
                    token = lookup(lexeme, subtopics, topics)
                result[-1][-1].append(token)
    return result
