import time
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

LogSeverityText={
    LogSeverity.debug: "DEBUG",
    LogSeverity.info: "INFO",
    LogSeverity.notice: "NOTICE",
    LogSeverity.warning: "WARNING",
    LogSeverity.err: "ERROR",
    LogSeverity.crit: "CRITICAL",
    LogSeverity.alert: "ALERT",
    LogSeverity.emrg: "EMRG"
    }

class LogWriter(object):
    
    def __init__(self, level):
        self.level = level

    def log(self, severity, module, message):
        pass

    def logDebug(self, module, message):
        self.log(LogSeverity.debug, module, message)


class MultiWriter(LogWriter):
    writers = []

    def __init__(self):
        pass

    def addWriter(self, writer):
        self.writers.append(writer)

    def log(self, severity, module, message):
        for writer in self.writers:
            writer.log(severity, module, message)

class ConsoleWriter(LogWriter):

    def log(self, severity, module, message):
        if severity.value >= self.level.value:
            print "{date} {severity} {module}: {msg}".format(date=time.strftime("%c"), severity=LogSeverityText[severity], module=module, msg=message)

class FileWriter(LogWriter):

    def __init__(self, level, file):
        self.filename = file
        super(FileWriter, self).__init__(level)

    def log(self, severity, module, message):
        if severity.value >= self.level.value:
            f = open(self.filename, "a")
            f.write("{date} {severity} {module}: {msg}\n".format(date=time.strftime("%c"), severity=LogSeverityText[severity], module=module, msg=message))
            f.close()



#logger = MultiWriter()
#logger.addWriter(ConsoleWriter(LogSeverity.debug))
