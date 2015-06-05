from . import Noun
from plain_english.language.pragmatics.verbs.is_ import is_
from plain_english.language.pragmatics.verbs.has_ import has_


class Entity(Noun):
    prototype = {
        'is_': is_,
        'has_': has_,
    }
