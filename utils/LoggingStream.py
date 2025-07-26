from PySide6.QtCore import Signal
from PySide6.QtCore import QObject
import sys
import logging


class QtLoggingStreamHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.widget = None

    def add_widget(self, widget):
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)

        # Define colors based on log level
        level = record.levelno
        if level >= logging.CRITICAL:
            color = "magenta"
        elif level >= logging.ERROR:
            color = "red"
        elif level >= logging.WARNING:
            color = "orange"
        elif level >= logging.INFO:
            color = "green"
        else:
            color = "blue"

        # Append colored text using HTML
        formatted_msg = f'<span style="color:{color};">{msg}</span>'
        if self.widget:
            self.widget.append(formatted_msg)


# ANSI color codes
COLOR_RESET = "\033[0m"
COLORS = {
    logging.DEBUG: "\033[94m",  # Blue
    logging.INFO: "\033[92m",  # Green
    logging.WARNING: "\033[93m",  # Yellow
    logging.ERROR: "\033[91m",  # Red
    logging.CRITICAL: "\033[95m"  # Magenta
}


class ColorFormatter(logging.Formatter):
    def format(self, record):
        color = COLORS.get(record.levelno, COLOR_RESET)
        record.msg = f"{color}{record.msg}{COLOR_RESET}"
        return super().format(record)


def setup_logger():
    # create logger called 'Stefano' con livello DEBUG
    logger = logging.getLogger('Stefano')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    file_logging_handler = logging.FileHandler('Stefano.log')
    file_logging_handler.setLevel(logging.DEBUG)
    file_logging_handler.name = "file_logging"
    # create console handler with
    console_logging_handler = logging.StreamHandler()
    console_logging_handler.setLevel(logging.DEBUG)
    console_logging_handler.name = "console_logging"

    # create PyQt handler which logs INFO message
    qt_logging_handler = QtLoggingStreamHandler()
    qt_logging_handler.setLevel(logging.DEBUG)
    qt_logging_handler.name = "qt_logging"

    # formatter = logging.Formatter(fmt=("[%(asctime)s %(levelname)8s]: %(message)s"), datefmt="%H:%M:%S")
    # logger.addHandler(qt_logging_handler)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(fmt=("[%(levelname)s] %(asctime)s %(message)s"), datefmt="%H:%M:%S")
    color_formatter = ColorFormatter(fmt=("[%(levelname)s] %(asctime)s %(message)s"), datefmt="%H:%M:%S")

    # file_logging_handler.setFormatter(formatter)
    # console_logging_handler.setFormatter()
    # qt_logging_handler.setFormatter(formatter)

    file_logging_handler.setFormatter(formatter)
    qt_logging_handler.setFormatter(formatter)
    console_logging_handler.setFormatter(color_formatter)

    # add the handlers to the logger
    logger.addHandler(file_logging_handler)
    logger.addHandler(qt_logging_handler)
    logger.addHandler(console_logging_handler)

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
