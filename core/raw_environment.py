class RawEnvironment(object):
    def __init__(self):
        self.frame = {}
        self.triggers = {}
        self.todos = []

    def set(self, name, value):
        self.frame[name] = value

    def get(self, name):
        return self.frame.get(name, None)

    def register(self, trigger, callback):
        self.triggers[trigger] = callback

    def trigger(self, trigger, value):
        print trigger
        self.triggers.get(trigger, lambda env, value: None)(self, value)

    def todo(self, callback):
        self.todos.append(callback)

    def step(self):
        if self.todos:
            self.todos.pop(0)()
        else:
            exit()
