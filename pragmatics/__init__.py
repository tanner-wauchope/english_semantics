from plain_english.pragmatics import nouns
from plain_english.pragmatics.content_words import quote, number
from plain_english.pragmatics.function_words import a, every, that, the


def populate_scope(scope):
    scope['a'] = a.IndefiniteArticle(scope)
    scope['the'] = the.DefiniteArticle(scope)
    scope['every'] = every.Distributor(scope)
    scope['Quote'] = nouns.Group(noun=quote.Quote, scope=scope)
    scope['Number'] = nouns.Group(noun=number.Number, scope=scope)
    scope['that'] = that.Complementizer()
