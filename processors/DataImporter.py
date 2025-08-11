import pandas as pd
import math
from data.WalletData import WalletData
from data.CategoryStructure import CategoryStructure
import logging

logger = logging.getLogger("Stefano")


class DataImporter:

    def __init__(self, filename, main_wallet_selection=True, start_date=None, end_date=None, ):
        self.input_filename = filename
        self.wallet_data = None
        self.start_date = start_date
        self.end_date = end_date

        self.import_file(main_wallet_selection=main_wallet_selection)
        self.filter_data_by_time()

    def import_file(self, main_wallet_selection):
        all_data = pd.read_excel(self.input_filename)
        self.wallet_data = WalletData(all_data, main_wallet_selection)
        logger.info("Importing data from .csv: DONE")
        del all_data

    def filter_data_by_time(self):
        if not isinstance(self.wallet_data, WalletData):
            logger.error("get_time_filtered_data(): Wrong input type for data")
            raise TypeError

        try:
            timestamp_start_date = pd.Timestamp(self.start_date + " " + "00:00:00")
        except Exception as e:
            logger.error("Error in timestamp_start_date()", e)
            raise TypeError

        try:
            timestamp_end_date = pd.Timestamp(self.end_date + " " + "23:59:59")
        except Exception as e:
            logger.error("Error in timestamp_end_date()", e)
            raise TypeError

        self.wallet_data.all_data = self.wallet_data.all_data[(self.wallet_data.all_data["date"] >= timestamp_start_date) &
                                                  (self.wallet_data.all_data["date"] <= timestamp_end_date)]
        self.wallet_data.all_data.reset_index(inplace=True, drop=True)
        logger.info("Filtering data by start and end time selected: DONE")

    def get_imported_data(self) -> WalletData:
        return self.wallet_data
