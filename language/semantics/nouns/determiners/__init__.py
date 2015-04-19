from language.semantics.nouns.determiners.the import is_singular

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
