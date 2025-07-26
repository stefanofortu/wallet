import json
import logging

logger = logging.getLogger("Stefano")


class ProjectData:
    def __init__(self):
        self.project_file_name = "ProjectData.json"
        self.input_file_name = ""
        self.main_wallets = True
        self.start_date_selected = ""
        self.end_date_selected = ""
        self.read_project_file()

    def set_input_file_name(self, input_filename):
        if not isinstance(input_filename, str):
            print("ProjectData().set_main_wallets: main_wallets is not bool")
        self.input_file_name = input_filename
        self.write_project_file()

    def set_main_wallets(self, main_wallets):
        if not isinstance(main_wallets, bool):
            print("ProjectData().set_main_wallets: main_wallets is not bool")
        self.main_wallets = main_wallets
        self.write_project_file()

    def set_start_date_selected(self, start_date):
        self.start_date_selected = start_date
        self.write_project_file()

    def set_end_date_selected(self, end_date):
        self.end_date_selected = end_date
        self.write_project_file()

    def read_project_file(self):
        try:
            with open(self.project_file_name, 'r') as in_file:
                # Reading from json file
                json_dict = json.load(in_file)
                self.input_file_name = json_dict["input_file_name"]
                self.main_wallets = json_dict["main_wallets"]
                self.start_date_selected = json_dict["start_date_selected"]
                self.end_date_selected = json_dict["end_date_selected"]
        except OSError:
            logger.error("Project file not found")
            self.input_file_name = ""
            self.main_wallets = True
            self.start_date_selected = ""
            self.end_date_selected = ""
            self.write_project_file()
        except:
            logger.error("Error in opening project file")

    def write_project_file(self):
        output_dict = {
            "input_file_name": self.input_file_name,
            "main_wallets": self.main_wallets,
            "start_date_selected": self.start_date_selected,
            "end_date_selected": self.end_date_selected
        }

        with open(self.project_file_name, "w") as out_file:
            json.dump(output_dict, out_file, indent=4)
