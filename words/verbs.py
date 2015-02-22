from . import Verb, ActionVerb, StativeVerb

be = StativeVerb('be')
be.singular_form = 'is'
be.plural_form = 'are'

has = StativeVerb('have')
has.singular_form = 'has'

do = ActionVerb('do')
do.singular_form = 'does'