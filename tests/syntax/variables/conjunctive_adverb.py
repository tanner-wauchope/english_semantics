from language.syntax.discourse import interpret


def trailing_conjunctive_adverb():
    assert interpret("say it otherwise") == "say(it).otherwise"

def leading_conjunctive_adverb():
    assert interpret("otherwise, say it") == "otherwise(say(it))"