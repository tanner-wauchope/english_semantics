class Word:
    COMPLEMENTS = []
    SPECIFIES = []
    REQUIRES_SPECIFIER = False
    REQUIRES_COMPLEMENT = False
    DEFAULT_SPECIFIER = None
    DEFAULT_COMPLEMENT = None

    def __init__(self, spelling, meaning, **kwargs):
        self.spelling = spelling
        self.meaning = meaning
        self._complements = kwargs.get("Complements")
        self._specifies = kwargs.get("Specifies")
        self._complement_default = kwargs.get("Complement Default")
        self._specifier_default = kwargs.get("Specifier Default")

    def __str__(self):
        return self.spelling

    @property
    def complements_types(self):
        if self._complements is not None:
            return self._complements
        return self.__class__.COMPLEMENTS

    @property
    def specifies_types(self):
        if self._specifies is not None:
            return self._specifies
        return self.__class__.SPECIFIES

    @property
    def default_complement(self):
        if self._default_complement:
            return self._default_complement()
        elif self.__class__.DEFAULT_COMPLEMENT:
            return self.DEFAULT_COMPLEMENT()

    @property
    def default_specifier(self):
        if self._default_specifier:
            return self._default_specifier()
        elif self.__class__.DEFAULT_SPECIFIER:
            return self.DEFAULT_SPECIFIER()

    def complements(self, other):
        for Type in self.complements_types():
            if isinstance(other, Type):
                return True

    def specifies(self, other):
        for Type in self.specifies_types():
            if isinstance(other, Type):
                return True