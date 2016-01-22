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

class EnumS(String):
    
    def __init__(self, options, optional=True):
        self.optional = optional
        self.options = options        
        self.type = 'Enum'

class EnumI(Integer):
    
    def __init__(self, options, optional=True):
        self.optional = optional
        self.options = options        
        self.type = 'Enum'

class JSON(Option):
    
    def value(self, input):
        import json
        import jinja2.runtime
        import pprint
        try:
            pprint.pprint(input)
            return json.dumps(input)
        except Exception as e:
            return ""


    def parse(self, input):
        import json
        return json.loads(input)

class PasswordDB(EnumS):
    
    def __init__(self, optional=True):
        import ScoringEngine.db
        import ScoringEngine.db.tables
        session = ScoringEngine.db.Session()
        self.optional = optional
        self.options = []
        for o in session.query(ScoringEngine.db.tables.PasswordDatabase.db).distinct():
            self.options.append(o[0])
        self.type = 'Enum'

