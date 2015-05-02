from language.syntax.word_classes import (
    keywords,
    number,
    possessive,
    quote,
    topic,
    noun,
    verb,
)


def classify(lexeme):
    """
    :param lexeme: a lexeme that is possibly punctuated or numeric
    :return: the word class of the lexeme
    """
    if number.match(lexeme):
        return number.Number
    elif quote.match(lexeme):
        return quote.Quote
    elif possessive.match(lexeme):
        return possessive.Possessive
    elif topic.match(lexeme):
        return topic.Topic
    elif lexeme in keywords:
        return keywords[lexeme]
    elif noun.match(lexeme):
        return noun.Noun
    elif verb.match(lexeme):
        return verb.Verb
    raise NameError(lexeme + ' is not a valid token.')


def tokenize(paragraph):
    """
    Replaces the lexemes in the paragraph with tokens.
    :param paragraph: sentences that contain lines that contain lexemes
    :return: sentences that contain lines that contain tokens
    """
    tokens = []
    for sentence in paragraph:
        tokens.append([])
        for line in sentence:
            tokens[-1].append([])
            for lexeme in line:
                word_class = classify(lexeme)
                token = word_class(lexeme)
                tokens[-1][-1].append(token)
    return tokens
