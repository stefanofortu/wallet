from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon
from icons.resources import resource_path
from processors.MainWidget import MainWidget


class Project_Data:
    def __init__(self):
        self.input_file_name = ""
        self.year_selection_combobox = ""

    def set_input_file_name(self, input_filename):
        self.input_file_name = input_filename

    def set_year_selection_combobox(self, year_selection_combobox):
        self.year_selection_combobox = year_selection_combobox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project_data = Project_Data()
        self.project_data.input_file_name = "C:/Users/Stefano/Documents/MEGA/MegaSync_Pixel/report_2024-09-08_175633.xls"
        self.project_data.year_selection_combobox = "2023"
        self.setWindowTitle("Wallet check")
        self.left = 100
        self.top = 100
        self.width = 360
        self.height = 120
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color: rgb(255,255,255)")

        self.main_widget = MainWidget(self.project_data)
        self.setCentralWidget(self.main_widget)
        self.setWindowIcon(QIcon(resource_path("test_new.png")))
