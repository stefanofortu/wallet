from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QGridLayout, \
    QFileDialog, QTextBrowser, QDateEdit, QCheckBox
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QComboBox
from icons.resources import resource_path
from processors.WalletProcessor import WalletProcessor
from utils.LoggingStream import LoggingStream
import logging, os

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
        btn_input_file_selector = QPushButton("Add ")
        btn_input_file_selector.setIcon(QIcon(resource_path("folder-icon.jpg")))
        btn_input_file_selector.pressed.connect(self.openInputFileDialog)
        input_file_layout.addWidget(btn_input_file_selector, 1, 8, 1, 1)
        ##
        widget_main_layout.addLayout(input_file_layout)

        year_selection_combobox_layout = QHBoxLayout()
        self.year_selection_checkbox = QCheckBox("Select year")
        self.year_selection_checkbox.setChecked(True)
        self.year_selection_checkbox.stateChanged.connect(self.year_selection_checkbox_toggled)
        self.year_selection_combobox = QComboBox()
        self.year_selection_combobox.addItems([str(x) for x in range(2018, 2026)])
        self.year_selection_combobox.setCurrentText(self.project_data.year_selected)
        self.year_selection_combobox.currentTextChanged.connect(self.save_year_selected)
        self.year_selection_combobox.setEnabled(True)

        self.start_end_date_checkbox = QCheckBox("Select time period")
        self.start_end_date_checkbox.setChecked(False)
        self.start_end_date_checkbox.stateChanged.connect(self.start_end_date_checkbox_toggled)
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.fromString(self.project_data.start_date_selected, "yyyy-MM-dd"))
        self.start_date_edit.dateChanged.connect(self.save_start_date_selected)
        self.start_date_edit.setEnabled(False)
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.fromString(self.project_data.end_date_selected, "yyyy-MM-dd"))
        self.end_date_edit.dateChanged.connect(self.save_end_date_selected)
        self.end_date_edit.setEnabled(False)

        year_selection_combobox_layout.addWidget(self.year_selection_checkbox)
        year_selection_combobox_layout.addWidget(self.year_selection_combobox)
        year_selection_combobox_layout.addStretch()
        year_selection_combobox_layout.addWidget(self.start_end_date_checkbox)
        year_selection_combobox_layout.addWidget(self.start_date_edit)
        year_selection_combobox_layout.addWidget(self.end_date_edit)
        widget_main_layout.addLayout(year_selection_combobox_layout)

        ############### ELABORATION  ###############
        exec_row_layout = QHBoxLayout()
        exec_row_layout.addStretch()
        btn_exec_tc_substitution = QPushButton("Start substitution")
        btn_exec_tc_substitution.setIcon(QIcon(resource_path('execute-icon.jpg')))
        btn_exec_tc_substitution.pressed.connect(self.tc_substitution_exec_conversion)
        exec_row_layout.addWidget(btn_exec_tc_substitution)

        exec_row_layout.addStretch()

        widget_main_layout.addLayout(exec_row_layout)

        ############### LOGGING  ###############
        self.logging_text_browser = QTextBrowser(self)
        LoggingStream.stdout().messageWritten.connect(self.logging_text_browser.insertPlainText)
        LoggingStream.stderr().messageWritten.connect(self.logging_text_browser.insertPlainText)
        widget_main_layout.addWidget(self.logging_text_browser)
        ############### SET MAIN LAYOUT
        self.setLayout(widget_main_layout)
        ############### GUI END

    def tc_substitution_exec_conversion(self):
        self.logging_text_browser.clear()
        if self.year_selection_checkbox.isChecked():
            wallet_processor = WalletProcessor(input_filename=self.input_file_path_label.text(),
                                               time_period=self.year_selection_combobox.currentText(),
                                               start_date=None,
                                               end_date=None
                                               )
        if self.start_end_date_checkbox.isChecked():
            wallet_processor = WalletProcessor(input_filename=self.input_file_path_label.text(),
                                               time_period=None,
                                               start_date=self.start_date_edit.date().toString("yyyy-MM-dd"),
                                               end_date=self.end_date_edit.date().toString("yyyy-MM-dd")
                                               )
        wallet_processor.execute()

    def openInputFileDialog(self):
        last_dir_path = os.path.dirname(self.project_data.input_file_name)
        fileName, _ = QFileDialog.getOpenFileName(self, caption="Select input xlsx file", dir=last_dir_path,
                                                  filter="All Files (*);;Excel Files (*.xlsx);;Excel Files (*.xls) ",
                                                  selectedFilter="Excel Files (*.xls)")
        if fileName:
            logger.info("file selected: %s", str(fileName))
            self.input_file_path_label.setText(fileName)
            self.project_data.set_input_file_name(input_filename=fileName)

    def save_year_selected(self, text):
        self.project_data.set_year_selected(text)

    def save_start_date_selected(self, qdate):
        self.project_data.set_start_date_selected(qdate.toString("yyyy-MM-dd"))

    def save_end_date_selected(self, qdate):
        self.project_data.set_end_date_selected(qdate.toString("yyyy-MM-dd"))

    def year_selection_checkbox_toggled(self):
        if self.year_selection_checkbox.isChecked():
            self.start_end_date_checkbox.setChecked(False)
            self.start_date_edit.setEnabled(False)
            self.end_date_edit.setEnabled(False)
        else:
            self.start_end_date_checkbox.setChecked(True)
            self.start_date_edit.setEnabled(True)
            self.end_date_edit.setEnabled(True)

    def start_end_date_checkbox_toggled(self):
        if self.start_end_date_checkbox.isChecked():
            self.year_selection_checkbox.setChecked(False)
            self.year_selection_combobox.setEnabled(False)
        else:
            self.year_selection_checkbox.setChecked(True)
            self.year_selection_combobox.setEnabled(True)
