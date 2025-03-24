from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QGridLayout, \
    QFileDialog, QTextBrowser
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QComboBox
from icons.resources import resource_path
from processors.WalletProcessor import WalletProcessor
from utils.LoggingStream import LoggingStream
import logging

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
        self.year_selection_combobox = QComboBox()
        self.year_selection_combobox.addItems([str(x) for x in range(2018, 2025)])
        self.year_selection_combobox.setCurrentText(self.project_data.year_selected)
        self.year_selection_combobox.currentTextChanged.connect(self.set_year_selected)
        year_selection_combobox_layout.addStretch(1)
        year_selection_combobox_layout.addWidget(self.year_selection_combobox, stretch=2)
        year_selection_combobox_layout.addStretch(1)

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
        logging_text_browser = QTextBrowser(self)
        LoggingStream.stdout().messageWritten.connect(logging_text_browser.insertPlainText)
        LoggingStream.stderr().messageWritten.connect(logging_text_browser.insertPlainText)
        widget_main_layout.addWidget(logging_text_browser)
        ############### SET MAIN LAYOUT
        self.setLayout(widget_main_layout)
        ############### GUI END

    def tc_substitution_exec_conversion(self):
        wallet_processor = WalletProcessor(input_filename=self.input_file_path_label.text(),
                                           time_period=self.year_selection_combobox.currentText())
        wallet_processor.execute()

    def openInputFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select input xlsx file", "",
                                                  "All Files (*);;Excel Files (*.xlsx);;Excel Files (*.xls) ")
        if fileName:
            logger.info(fileName)
            self.input_file_path_label.setText(fileName)
            self.project_data.set_input_file_name(input_filename=fileName)

    def set_year_selected(self, text):
        self.project_data.set_year_selected(text)
