from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QGridLayout, \
    QFileDialog, QTextBrowser, QDateEdit, QCheckBox
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QIcon
from icons.resources import resource_path
from processors.WalletProcessor import WalletProcessor

import logging, os

from utils.LoggingStream import df_logger
logger = logging.getLogger("Stefano")


class MainWidget(QWidget):
    def __init__(self, project_data):
        super().__init__()
        self.project_data = project_data
        widget_main_layout = QVBoxLayout()
        ############### INPUT FILE  ###############
        input_file_layout = QGridLayout()
        #
        input_file_description_label = QLabel(self)
        input_file_description_label.setText("Input file :")
        input_file_description_label.setAlignment(Qt.AlignLeft)
        input_file_layout.addWidget(input_file_description_label, 0, 0)
        #
        self.input_file_path_label = QLabel(self)
        self.input_file_path_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.input_file_path_label.setText(self.project_data.input_file_name)
        self.input_file_path_label.setAlignment(Qt.AlignLeft)
        input_file_layout.addWidget(self.input_file_path_label, 1, 0, 1, 8)
        #
        btn_input_file_selector = QPushButton("Select file")
        btn_input_file_selector.setIcon(QIcon(resource_path("excel.png")))
        btn_input_file_selector.pressed.connect(self.openInputFileDialog)
        input_file_layout.addWidget(btn_input_file_selector, 1, 8, 1, 1)
        ##
        widget_main_layout.addLayout(input_file_layout)

        wallets_selection_layout = QVBoxLayout()
        self.main_wallet_checkbox = QCheckBox("Main wallet")

        self.main_wallet_checkbox.setChecked(self.project_data.main_wallets)
        self.main_wallet_checkbox.stateChanged.connect(self.main_wallet_checkbox_toggled)
        self.home_wallet_checkbox = QCheckBox("Home wallets")
        self.home_wallet_checkbox.setChecked(not self.project_data.main_wallets)
        self.home_wallet_checkbox.stateChanged.connect(self.home_wallet_checkbox_toggled)

        wallets_selection_layout.addWidget(self.main_wallet_checkbox)
        wallets_selection_layout.addWidget(self.home_wallet_checkbox)

        start_date_layout = QVBoxLayout()
        self.start_date_label = QLabel(self)
        self.start_date_label.setText("Start date")
        self.start_date_label.setAlignment(Qt.AlignLeft)
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.fromString(self.project_data.start_date_selected, "yyyy-MM-dd"))
        self.start_date_edit.dateChanged.connect(self.save_start_date_selected)
        self.start_date_edit.setEnabled(True)
        start_date_layout.addWidget(self.start_date_label)
        start_date_layout.addWidget(self.start_date_edit)

        end_date_layout = QVBoxLayout()
        self.end_date_label = QLabel(self)
        self.end_date_label.setText("End date: ")
        self.end_date_label.setAlignment(Qt.AlignLeft)
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.fromString(self.project_data.end_date_selected, "yyyy-MM-dd"))
        self.end_date_edit.dateChanged.connect(self.save_end_date_selected)
        self.end_date_edit.setEnabled(True)
        end_date_layout.addWidget(self.end_date_label)
        end_date_layout.addWidget(self.end_date_edit)

        wallet_time_selection_layout = QHBoxLayout()
        wallet_time_selection_layout.addLayout(wallets_selection_layout)
        wallet_time_selection_layout.addStretch()
        wallet_time_selection_layout.addLayout(start_date_layout)
        wallet_time_selection_layout.addStretch()
        wallet_time_selection_layout.addLayout(end_date_layout)

        widget_main_layout.addLayout(wallet_time_selection_layout)

        ############### ELABORATION  ###############
        exec_row_layout = QHBoxLayout()
        exec_row_layout.addStretch()
        btn_exec_tc_substitution = QPushButton("Calculate Summary")
        btn_exec_tc_substitution.setIcon(QIcon(resource_path('execute-icon.jpg')))
        btn_exec_tc_substitution.pressed.connect(self.tc_substitution_exec_conversion)
        exec_row_layout.addWidget(btn_exec_tc_substitution)
        exec_row_layout.addStretch()

        widget_main_layout.addLayout(exec_row_layout)

        ############### LOGGING  ###############
        self.logging_text_browser = QTextBrowser(self)
        # LoggingStream.stdout().messageWritten.connect(self.logging_text_browser.insertPlainText)
        # LoggingStream.stderr().messageWritten.connect(self.logging_text_browser.insertPlainText)
        for handler in logger.handlers:
            if hasattr(handler, "name"):
                if handler.name == "qt_text_browser_logging":
                    handler.add_widget(self.logging_text_browser)
        df_logger.log_signal.connect(self.append_log)
        widget_main_layout.addWidget(self.logging_text_browser)
        ############### CLEAR BUTTON  ###############
        clear_row_layout = QHBoxLayout()
        clear_row_layout.addStretch()
        btn_clear_window = QPushButton("Clear window")
        btn_clear_window.setIcon(QIcon(resource_path('cleanup-icon-small.jpg')))
        btn_clear_window.pressed.connect(self.clear_window)
        clear_row_layout.addWidget(btn_clear_window)
        widget_main_layout.addLayout(clear_row_layout)
        ############### SET MAIN LAYOUT
        self.setLayout(widget_main_layout)
        ############### GUI END

    def tc_substitution_exec_conversion(self):
        self.logging_text_browser.clear()
        wallet_processor = WalletProcessor(input_filename=self.input_file_path_label.text(),
                                           main_wallet_selection=self.main_wallet_checkbox.isChecked(),
                                           start_date=self.start_date_edit.date().toString("yyyy-MM-dd"),
                                           end_date=self.end_date_edit.date().toString("yyyy-MM-dd")
                                           )
        wallet_processor.execute()

    def clear_window(self):
        self.logging_text_browser.clear()

    def openInputFileDialog(self):
        last_dir_path = os.path.dirname(self.project_data.input_file_name)
        fileName, _ = QFileDialog.getOpenFileName(self, caption="Select input xlsx file", dir=last_dir_path,
                                                  filter="All Files (*);;Excel Files (*.xlsx);;Excel Files (*.xls) ",
                                                  selectedFilter="Excel Files (*.xls)")
        if fileName:
            logger.info("file selected: %s", str(fileName))
            self.input_file_path_label.setText(fileName)
            self.project_data.set_input_file_name(input_filename=fileName)
            self.logging_text_browser.clear()

    def save_year_selected(self, text):
        self.project_data.set_year_selected(text)

    def save_start_date_selected(self, qdate):
        self.project_data.set_start_date_selected(qdate.toString("yyyy-MM-dd"))

    def save_end_date_selected(self, qdate):
        self.project_data.set_end_date_selected(qdate.toString("yyyy-MM-dd"))

    def main_wallet_checkbox_toggled(self):
        if self.main_wallet_checkbox.isChecked():
            self.home_wallet_checkbox.setChecked(False)
            self.project_data.set_main_wallets(True)

        else:
            self.home_wallet_checkbox.setChecked(True)
            self.project_data.set_main_wallets(False)

    def home_wallet_checkbox_toggled(self):
        if self.home_wallet_checkbox.isChecked():
            self.main_wallet_checkbox.setChecked(False)
            self.project_data.set_main_wallets(False)
        else:
            self.main_wallet_checkbox.setChecked(True)
            self.project_data.set_main_wallets(True)

    def append_log(self, log_text: str):
        """Slot to update QTextBrowser."""
        self.logging_text_browser.append(f"{log_text}")
