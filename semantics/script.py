from plain_english.semantics import entity


class Say(entity.Relation):
    pass


class Script(entity.Entity):
    say_ = Say('say_')
