

class Instance:
    def __init__(self, kind, actions, states):
        self.kind = kind
        self.actions = actions
        self.states = states

    def assign_action(self, verb, other):
        for instance in other.instances:
            instance._actions.get(verb, []).append(other)
        else:
            self.actions.get(verb, []).append(other.kind)

    def assign_state(self, verb, other):
        for instance in other.instances:
            instance._states.get(verb, []).append(other)
        else:
            self.states.get(verb, []).append(other.kind)

class Kind:
    def __init__(self):
        self.instances = {}
        self.actions = []
        self.states = []

    def create(self, key, actions=[], states=[]):
        instance = Instance(self, actions, states)
        self.instances[key] = instance
        return instance

    def assign_action(self, verb, other):
        for instance in other.instances:
            instance.actions.get(verb, []).append(other)
        else:
            self.actions.get(verb, []).append(other.kind)

    def assign_state(self, verb, other):
        for instance in other.instances:
            instance.states.get(verb, []).append(other)
        else:
            self.states.get(verb, []).append(other.kind)

class WorkSet:
    discourse = []

    def __init__(self, kind, definite=False, singular=False):
        self.kind = kind
        self.instances = self.load_instances(definite, singular)

    def instances(self, definite, singular):
        if definite and singular:
            return self.most_recent()
        elif definite and not singular:
            return self.recent()
        elif not definite and singular:
            return self.kind.create()

    def most_recent(self):
        for instance in self.__class__.discourse:
            if instance in self.kind.instances:
                return instance

    def recent(self):
        result = []
        for instance in self.__class__.discourse:
            if instance in self.kind.instances:
                result.append(instance)
        return result

    def add_predicate(self, verb, other):
        for instance in self.instances:
            instance.add_predicate(verb, other)
        if not self.instances:
            self.kind.add_predicate(verb, other)

    def get_predicate(self, verb, other):
        for instance in self.instances:
            if not instance.get_predicate(verb, other):
                return False
        if not self.instances:
            return self.kind.get_predicate(verb, other)



