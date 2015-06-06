from . import Noun
from plain_english.pragmatics.verbs import has_, is_


class Entity(Noun):
    prototype = {
        'is_': is_,
        'has_': has_,
    }
