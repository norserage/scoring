import datetime
from enum import Enum

class LogSeverity(Enum):
    debug = 1
    info = 2
    notice = 3
    warning = 4
    err = 5
    crit = 6
    alert = 7
    emrg = 8

class LogWriter():
    
    def __init__(self, level):
        self.level = level

    def log(self, severity, module, message):
        if severity >= self.level:
            write("{date} {level} {"

    def log(self, severity, message):
        self.log(severity, "", message)

    def logDebug(self, module, message):
        log(LogSeverity.debug, module, message)

    def logDebug(self, message):
        logDebug("", message)

    def write(self, text):
        pass

class MultiWriter(LogWriter):
    writers = []

    def __init__(self):
        return super(MultiWriter, self).__init__(LogSeverity.debug)

    def addWriter(self, writer):
        self.writers.append(writer)
    
    def write(self, text):
        for writer in self.writers:
            writer.write(text)

class ConsoleWriter(LogWriter):
    def write(self, text):
        print text

class FileWriter(LogWriter):
    def write(self, text):
        pass


logger = MultiWriter()
logger.addWriter(ConsoleWriter(LogSeverity.debug))
