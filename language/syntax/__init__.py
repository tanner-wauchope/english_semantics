from .scan import scan
from .tokenize import tokenize
from .parse import parse
from .generate import generate
from .warn import warn

from language.syntax.variables import (
    Complementizer,
    Determiner,
    Noun,
    Subordinator,
    Verb,
)

# Complementizers
that_ = Complementizer
whose_ = Complementizer

# Determiners
a_ = Determiner
an_ = Determiner
the_ = Determiner
each_ = Determiner
any_ = Determiner

# Nouns
it_ = Noun
number_ = Noun
quote_ = Noun

# Subordinators
if_ = Subordinator
otherwise_ = Subordinator

# Verbs
is_ = Verb
have_ = Verb