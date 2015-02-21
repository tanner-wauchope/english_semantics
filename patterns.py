import enum

class Pattern(enum.Enum):
    # Implement in subsequent versions
    BLOCK = r':'
    BRANCH = r'\n- '
    LONG_QUOTE = r'\n\t'

    # Implement Immediately
    WORD = r'[^ ]+'
    SHORT_QUOTE = r'"[^"]*"'
    NUMBER = r'-?\d+(\.\d+)?'

    # Keywords
    ARTICLE = "[a|the]"
    COMPARATIVE = "[more|less]"
    THAT = "that"
    WHOSE = "whose"
    NOT = "not"
    THAN = "than"





