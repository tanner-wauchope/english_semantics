from language.syntax.constituency import Constituency


def unify(constituencies):
    combination = True
    while len(constituencies) > 1 and combination:
        second_to_last, last = constituencies[:-2]
        combination = second_to_last.combine(last)
        if combination:
            constituencies[:-2] = [combination]
    return constituencies


class Parser:
    def __init__(self):
        self.trees = []

    def run(self, block):
        block_constituencies = []
        for line in block:
            line_constituencies = []
            for lexeme in line:
                line_constituencies.append(Constituency(lexeme))
                line_constituencies = unify(line_constituencies)
            block_constituencies.append(line_constituencies[0])
        self.trees.append(unify(block_constituencies))
        return self.trees[-1]
