import logging
import sys
from PySide6.QtWidgets import QApplication
from utils.LoggingStream import setup_logger
from processors.MainWindow import MainWindow

logger = logging.getLogger("Stefano")

if __name__ == '__main__':
    setup_logger()
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        logger.debug('PyInstaller bundle running')
        logger.debug("sys._MEIPASS : %s", sys._MEIPASS)
        logger.info(sys._MEIPASS)
    else:
        logger.debug('running in a normal Python process')

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())



