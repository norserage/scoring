
class Logger():
    def __init__(self, file):
        self.file = open(file, 'a')

    

logger = Logger("scoring.log")