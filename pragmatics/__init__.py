from plain_english.pragmatics.text import text
from plain_english.pragmatics.numbers import number
from plain_english.semantics import nouns
from plain_english.semantics.function_words import a, that, the
from plain_english.semantics.function_words import every


def populate_scope(scope):
    scope['a'] = a.IndefiniteArticle(scope)
    scope['the'] = the.DefiniteArticle(scope)
    scope['every'] = every.Distributor(scope)
    scope['Quote'] = nouns.Group(noun=text.Text, scope=scope)
    scope['Number'] = nouns.Group(noun=number.Number, scope=scope)
    scope['that'] = that.Complementizer()
