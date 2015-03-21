from parser import Word
from syntax.nouns.countable_nouns import is_singular


class NounPhrase(Constituency):
    @property
    def determiner(self):
        return self.specifier

    @property
    def noun(self):
        return self.head

    @property
    def verb(self):
        return self.complement

    def __repr__(self):
        return 'WorkSet({determiner} {noun}){verb}'.format(
            subject=repr(self.determiner), # includes a trailing comma
            verb=repr(self.noun),
            object=repr(self.operator),
        )



class Noun(Word):
    pass

class Article(Word):
    SPECIFIES_TYPES = [Noun]

    def agrees_phonetically(self, other):
        next_character = str(other)[0].lower()
        next_is_vowel = self.next_is_vowel
        return (
            next_is_vowel is None or
            next_is_vowel is True and next_character in 'aeiou' or
            next_is_vowel is False and next_character not in 'aeiou'
        )

    def direct_combine(self, other):
        if self.agrees_phonetically(other):
            return super(self, other).can_combine()

_a = Article('a', WorkSet(is_singular, definite=False))
_a.next_is_vowel = True
_an = Article('a', WorkSet(is_singular, definite=False))
_an.next_is_vowel = False
_the = Article('the', WorkSet(definite=True))
_the.next_is_vowel = None
