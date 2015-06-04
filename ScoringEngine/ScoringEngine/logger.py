from distutils.log import Log
import time
from datetime import datetime
from ScoringEngine.conf import conf
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
        if severity.value >= self.level.value:
            for n in message.split('\n'):
                self.writeEntry(severity, module, n)

    def logDebug(self, module, message):
        self.log(LogSeverity.debug, module, message)

    def logInfo(self, module, message):
        self.log(LogSeverity.info, module, message)

    def logNotice(self, module, message):
        self.log(LogSeverity.notice, module, message)

    def logWarning(self, module, message):
        self.log(LogSeverity.warning, module, message)

    def logError(self, module, message):
        self.log(LogSeverity.err, module, message)

    def logCritical(self, module, message):
        self.log(LogSeverity.crit, module, message)

    def logAlert(self, module, message):
        self.log(LogSeverity.alert, module, message)

    def writeEntry(self, severity, module, message):
        pass


class MultiWriter(LogWriter):
    writers = []

    def __init__(self):
        pass

    def addWriter(self, writer):
        self.writers.append(writer)

    def log(self, severity, module, message):
        for writer in self.writers:
            if severity.value >= writer.level.value:
                writer.log(severity, module, message)

class ConsoleWriter(LogWriter):
    def __init__(self, level, format="{date} {severity} {module}: {msg}"):
        self.format = format
        super(ConsoleWriter, self).__init__(level)

    def writeEntry(self, severity, module, message):
        if severity.value >= self.level.value:
            print self.format.format(date=time.strftime("%c"), severity=LogSeverityText[severity], module=module, msg=message)

class FileWriter(LogWriter):
    def __init__(self, level, file, format="{date} {severity} {module}: {msg}"):
        self.filename = file
        self.format = format
        super(FileWriter, self).__init__(level)

    def writeEntry(self, severity, module, message):
        if severity.value >= self.level.value:
            f = open(self.filename, "a")
            f.write((self.format + "\n").format(date=time.strftime("%c"), severity=LogSeverityText[severity], module=module, msg=message))
            f.close()

class MultiFileWriter(LogWriter):
    def __init__(self, level, path, format="{date} {severity} {module}: {msg}"):
        self.path = path
        self.format = format
        super(FileWriter, self).__init__(level)

    def writeEntry(self, severity, module, message):
        if severity.value >= self.level.value:
            f = open(self.path + "." + severity.name.lower(), "a")
            f.write((self.format + "\n").format(date=time.strftime("%c"), severity=LogSeverityText[severity], module=module, msg=message))
            f.close()



logger = MultiWriter()
if 'logger' not in conf:
    logger.addWriter(ConsoleWriter(LogSeverity.debug))
else:
    if 'console' in conf['logger']:
        if 'console_format' in conf['logger']:
            logger.addWriter(ConsoleWriter(LogSeverity[conf['logger']['console']], conf['logger']['console_format']))
        else:
            logger.addWriter(ConsoleWriter(LogSeverity[conf['logger']['console']]))
    if 'file' in conf['logger']:
        if 'file_path' not in conf['logger']:
            conf['logger']['file_path'] = "scoring.log" # Default log file path
        if 'file_format' in conf['logger']:
            logger.addWriter(FileWriter(LogSeverity[conf['logger']['file']], conf['logger']['file_path'], conf['logger']['file_format']))
        else:
            logger.addWriter(FileWriter(LogSeverity[conf['logger']['file']], conf['logger']['file_path']))
    if 'db' in conf['logger']:
        try:
            from ScoringEngine.db import tables, Session
            class DBWriter(LogWriter):
                def log(self, severity, module, message):
                    session = Session()
                    l = tables.Log()
                    l.time = datetime.now()
                    l.message = message
                    l.module = module
                    l.severity = severity.value
                    session.add(l)
            logger.addWriter(DBWriter(LogSeverity[conf['logger']['db']]))
        except Exception as e:
            pass