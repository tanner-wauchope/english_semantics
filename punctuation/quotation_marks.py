
class CircumpositionalElement:
    def __init__(self, text):
        if text[0] == self.opener and text[-1] == self.closer:
            self.body = text[len(self.opener):-len(self.closer)]
        else:
            raise ValueError("Missing delimiters: " + text)

    def __repr__(self):
        return '"' + self.body + '"'

    def __str__(self):
        return self.body

    def can_combine(self, other):
        return False

class Quote(CircumpositionalElement):
    opener = '"'
    closer = '"'

class Comment(CircumpositionalElement):
    opener = '('
    closer = ')'


