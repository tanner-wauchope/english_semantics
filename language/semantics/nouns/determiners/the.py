import warnings

from language.syntax.word_classes import Noun

def is_singular(noun):
    return isinstance(noun, SingularNoun)

def is_plural(noun):
    return isinstance(noun, PluralNoun)


class CountableNoun(Noun):
    REQUIRES_SPECIFIER = True


class SingularNoun(CountableNoun):


    def plural_spelling(self):
        spelling = self.spelling
        if self.soft_singular_ending():
            return spelling + 'es'
        elif spelling.endswith('y'):
            return spelling[:-1] + 'ies'
        else:
            return spelling + 's'

    def soft_singular_ending(self):
        for ending in ('s', 'ch', 'sh', 'x'):
            if self.spelling.endswith(ending):
                return True


class PluralNoun(CountableNoun):
    DEFAULT_SPECIFIER = _all

    def singular_spelling(self):
        spelling = self.spelling
        if self.soft_plural_ending():
            return spelling[:-2]
        elif spelling.endswith('ies'):
            return spelling[:-3] + 'y'
        elif spelling.endswith('s'):
            return spelling[:-1]
        else:
            warnings.warn('The singular spelling must be set manually.')

    def soft_plural_ending(self):
        for ending in ('ses', 'ches', 'shes', 'xes'):
            if self.spelling.endswith(ending):
                return True
