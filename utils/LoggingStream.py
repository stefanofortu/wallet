from PySide6.QtCore import Signal
from PySide6.QtCore import QObject
import sys
import logging


class LoggingStreamHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        record = self.format(record)
        if record:
            LoggingStream.stdout().write('%s\n' % record)


def setup_logger():
    # create logger called 'Stefano' con livello DEBUG
    logger = logging.getLogger('Stefano')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    file_logging_handler = logging.FileHandler('Stefano.log')
    file_logging_handler.setLevel(logging.DEBUG)
    # create console handler with
    console_logging_handler = logging.StreamHandler()
    console_logging_handler.setLevel(logging.DEBUG)
    # create PyQt handler which logs INFO message
    qt_logging_handler = LoggingStreamHandler()
    qt_logging_handler.setLevel(logging.WARNING)
    # formatter = logging.Formatter(fmt=("[%(asctime)s %(levelname)8s]: %(message)s"), datefmt="%H:%M:%S")
    # logger.addHandler(qt_logging_handler)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(fmt=("[%(levelname)s] %(asctime)s %(message)s"), datefmt="%H:%M:%S")
    file_logging_handler.setFormatter(formatter)
    console_logging_handler.setFormatter(formatter)
    qt_logging_handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(file_logging_handler)
    logger.addHandler(console_logging_handler)
    logger.addHandler(qt_logging_handler)


class LoggingStream(QObject):
    _stdout = None
    _stderr = None
    messageWritten = Signal(str)

    def flush(self):
        pass

    def fileno(self):
        return -1

    def write(self, msg):
        if not self.signalsBlocked():
            self.messageWritten.emit(msg)

    @staticmethod
    def stdout():
        if not LoggingStream._stdout:
            LoggingStream._stdout = LoggingStream()
            sys.stdout = LoggingStream._stdout
        return LoggingStream._stdout

    @staticmethod
    def stderr():
        if not LoggingStream._stderr:
            LoggingStream._stderr = LoggingStream()
            sys.stderr = LoggingStream._stderr
        return LoggingStream._stderr
