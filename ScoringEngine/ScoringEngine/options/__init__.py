"""
Copyright 2016 Brandon Warner

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
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
        for o in session.query(ScoringEngine.db.tables.PasswordDatabase.name).distinct():
            self.options.append(o[0])
        self.type = 'Enum'

