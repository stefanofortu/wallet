from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon
from icons.resources import resource_path
from processors.MainWidget import MainWidget
from processors.ProjectData import ProjectData
import logging

logger = logging.getLogger("Stefano")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project_data = ProjectData()
        self.setWindowTitle("Wallet check")
        self.left = 50
        self.top = 50
        self.width = 720
        self.height = 720
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color: rgb(218,228,231)")

        self.main_widget = MainWidget(self.project_data)
        self.setCentralWidget(self.main_widget)
        self.setWindowIcon(QIcon(resource_path("test_new.png")))
