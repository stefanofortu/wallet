import pandas as pd
import math

from data.WalletData import WalletData
from data.CategoryStructure import CategoryStructure


class DataImporter:

    def __init__(self, filename, year=None, start_date=None, end_date=None, ):
        self.input_filename = filename
        self.wallet_data = None
        self.import_file()
        self.select_personal_accounts()

        if year is not None:
            self.start_date = year + "-01-01"
            self.end_date = year + "-12-31"
        elif start_date is not None and end_date is not None:
            self.start_date = start_date
            self.end_date = end_date
        else:
            print("Error in year | start_data | end_date input")
            raise TypeError

        self.filter_data_by_time()
        self.verify_single_label()

    def get_imported_data(self) -> WalletData:
        return self.wallet_data

    def import_file(self):
        all_data = pd.read_excel(self.input_filename)
        self.wallet_data = WalletData(all_data)

    def select_personal_accounts(self):
        all_accounts = self.wallet_data.df['account'].unique()
        accounts_to_keep = list(["Cash", "Carta", "Banca", "Poste", "Barclays", "BPM"])
        account_to_be_removed = list(set(all_accounts) - set(accounts_to_keep))
        for account in account_to_be_removed:
            self.wallet_data.df = self.wallet_data.df.drop(
                self.wallet_data.df[self.wallet_data.df["account"] == account].index)
        self.wallet_data.df.reset_index(inplace=True, drop=True)

        accounts = list(self.wallet_data.df['account'].unique())
        account_remained = list(set(accounts) ^ set(accounts_to_keep))
        if len(account_remained) > 0:
            print("The following accounts are not present", account_remained)

    def verify_single_label(self):
        labels_imported = self.wallet_data.df['labels'].unique()
        wrong_label = False
        empty_label = False
        for label in labels_imported:
            if isinstance(label,str):
                if label != "in" and label != "out" and label != "risparmi":
                    wrong_label = True
            else:
                if math.isnan(label): # (labels_imported.isna()).any(axis=None):
                    empty_label = True

        if empty_label or wrong_label:
            print("all labels imported:", labels_imported)
            filtered_data = self.wallet_data.df[(self.wallet_data.df["labels"] != "in") &
                                                (self.wallet_data.df["labels"] != "out") &
                                                (self.wallet_data.df["labels"] != "risparmi")]
            print(filtered_data[['date', 'account', 'category', 'labels']])
            if wrong_label:
                raise ValueError('verify_single_label(). Label not in/out/savings')
            if empty_label:
                raise ValueError('verify_single_label(). Label empty')

    def filter_data_by_time(self):
        if not isinstance(self.wallet_data, WalletData):
            print("get_time_filtered_data(): Wrong input type for data")
            raise TypeError

        try:
            timestamp_start_date = pd.Timestamp(self.start_date + " " + "00:00:00")
        except Exception as e:
            print("Error in timestamp_start_date()", e)
            raise TypeError

        try:
            timestamp_end_date = pd.Timestamp(self.end_date + " " + "23:59:59")
        except Exception as e:
            print("Error in timestamp_end_date()", e)
            raise TypeError

        filtered_data = self.wallet_data.df[(self.wallet_data.df["date"] >= timestamp_start_date) &
                                            (self.wallet_data.df["date"] <= timestamp_end_date)]
        filtered_data.reset_index(inplace=True)
        self.wallet_data.df = filtered_data
