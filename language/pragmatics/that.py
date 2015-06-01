from plain_english.language.pragmatics.verbs import Clause, Verb


class RunOnComplementizer(Exception):
    pass



class Complementizer:
    def __call__(self, complement):
        if isinstance(complement, Verb):
            return Clause(conjugation=complement)
        elif complement.subject and complement.complement:
            raise RunOnComplementizer((self, complement))
        return complement

that = Complementizer()