

class Option():
    def __init__(self, optional=True):
        self.optional = optional
        self.type = self.__class__.__name__

    def value(self, input):
        return input

    def parse(self, input):
        return input

class String(Option):
    pass

class Integer(Option):
    pass

class Enum(Option):
    def __init__(self, options, optional=True):
        self.optional = optional
        self.options = options
        self.type = self.__class__.__name__
        pass