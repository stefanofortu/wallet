from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon
from icons.resources import resource_path
from processors.MainWidget import MainWidget
import json
import logging

logger = logging.getLogger("Stefano")


class Project_Data:
    def __init__(self):
        self.project_file_name = "ProjectData.json"
        self.input_file_name = ""
        self.year_selected = ""
        self.start_date_selected = ""
        self.end_date_selected = ""
        self.read_project_file()

    def set_input_file_name(self, input_filename):
        self.input_file_name = input_filename
        self.write_project_file()

    def set_year_selected(self, year_selected):
        self.year_selected = year_selected
        self.write_project_file()

    def set_start_date_selected(self, start_date):
        self.start_date = start_date
        self.write_project_file()

    def set_end_date_selected(self, end_date):
        self.end_date = end_date
        self.write_project_file()

    def read_project_file(self):
        try:
            with open(self.project_file_name, 'r') as in_file:
                # Reading from json file
                json_dict = json.load(in_file)
                self.input_file_name = json_dict["input_file_name"]
                self.year_selected = json_dict["year_selected"]
                self.start_date_selected = json_dict["start_date_selected"]
                self.end_date_selected = json_dict["end_date_selected"]
        except OSError:
            logger.error("project file not found")
            self.input_file_name = ""
            self.year_selected = ""
            self.write_project_file()
        except:
            logger.error("Error in opening project file")

    def write_project_file(self):
        output_dict = {
            "input_file_name": self.input_file_name,
            "year_selected": self.year_selected,
            "start_date_selected": self.start_date_selected,
            "end_date_selected": self.end_date_selected
        }

        with open(self.project_file_name, "w") as out_file:
            json.dump(output_dict, out_file, indent=4)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project_data = Project_Data()
        self.setWindowTitle("Wallet check")
        self.left = 100
        self.top = 100
        self.width = 360
        self.height = 120
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color: rgb(218,228,231)")

        self.main_widget = MainWidget(self.project_data)
        self.setCentralWidget(self.main_widget)
        self.setWindowIcon(QIcon(resource_path("test_new.png")))
