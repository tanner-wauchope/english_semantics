# plain_english
This package implements of a subset of the English language that can be compiled into Python. This project is currently in a pre-alpha state, but many tested modules have been written and more tested modules are coming soon.

The choice of keywords are inspired by the top-10, non-pronoun English words. These keywords can be organized into six logical groups:

1. Articles (a, the): These words add nouns to the current scope or look up instances in the current scope.
2. Auxiliary verbs (be, have): These words allow for inheritance, assignment, composition of classes.
3. The conjunction "and": This words allows sets of one type to be unioned and sets with disparate types to be tupled.
4. Adjectival prepositions (of, in): These words affect the set of instances that a noun phrase denotes.
5. Adverbial prepostions (to, for): These words allow extra parameters to be passed to statements and are also
                                    also allows for conditional introductory phrases of the form "For X that ..., do Y".
6. The complementizer "that": This word allows flexible filtering of the sets denoted by noun phrases.

Aside from the above keywords, this subset of English includes primitives and user-defined words. The acceptable primitives are:

1. Algebraic expressions: These expressions are enclosed in parentheses and may include numbers, arthmetic operators, and any variables or functions made available in the current scope.
2. Names: These expressions are enclosed in single quotes and indicate that a new token should be added to the current scope with the specified name. The motivation for this primitive type was to allow new words to be embedded in sentences while still ensuring that spelling errors do not accidentally introduce new words.
3. Text: This primitive is for literal text. When inlined, these expressions are enclosed in double quotes. When multiple lines are needed, indented block quotes are used.

This subset of English currently only includes two open word classes: nouns and verbs. Adjectives and adverbs will not be supported any time soon. The inflections of each word class that are supported are:

1. Nouns: singular, plural, possessive
2. Verbs: third-person present singular, third-person present plural

There are two limitations in the current implementation that are worth noting:

1. No side-effects have yet been added to the language. Consequently, the only way to use the packages are to import them in a Python file. I intend to begin work on an interactive interpreter soon.
2. The syntax specification currently depends on nouns being capitalized. Without this constraint, the syntax could not be context-free, because there would be no way to distinguish the part of speech of user-defined names without maintaining a symbol table during parsing. A mildly context-sensitive version of the parser will eventually be written, but for now, nouns are capitalized.

I'll do my best to keep this README up-to-date as more modules are fleshed out and tested.
