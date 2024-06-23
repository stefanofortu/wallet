import pandas as pd
from WalletData import WalletData


class DataImport:

    def __init__(self, _filename, _start_date, _end_date,):
        self.input_filename = _filename
        self.wallet_data = None
        self.start_date = _start_date
        self.end_date = _end_date
        self.import_file()
        self.select_personal_accounts()
        self.filter_data_by_time()

    def get_imported_data(self) -> WalletData:
        return self.wallet_data

    def import_file(self):
        all_data = pd.read_excel(self.input_filename)
        self.wallet_data = WalletData(all_data)

    def select_personal_accounts(self):
        all_accounts = self.wallet_data.df['account'].unique()
        accounts_to_keep = list(["Cash", "Carta", "Banca", "Poste", "Barclays"])
        account_to_be_removed = list(set(all_accounts) - set(accounts_to_keep))
        for account in account_to_be_removed:
            self.wallet_data.df = self.wallet_data.df.drop(self.wallet_data.df[self.wallet_data.df["account"] == account].index)
        self.wallet_data.df.reset_index(inplace=True, drop=True)

        accounts = list(self.wallet_data.df['account'].unique())
        account_remained = list(set(accounts) ^ set(accounts_to_keep))
        if len(account_remained) > 0:
            print("The following accounts are not present", account_remained)

    def filter_data_by_time(self):
        if not isinstance(self.wallet_data, WalletData):
            print("get_time_filtered_data(): Wrong input type for data")
            raise (TypeError)

        try:
            timestamp_start_date = pd.Timestamp(self.start_date)
        except:
            print("Error in timestamp_start_date()")
            raise (TypeError)
        try:
            timestamp_end_date = pd.Timestamp(self.end_date)
        except:
            print("Error in timestamp_end_date()")
            raise (TypeError)
        filtered_data = self.wallet_data.df[(self.wallet_data.df["date"] > timestamp_start_date) &
                                            (self.wallet_data.df["date"] < timestamp_end_date)]
        filtered_data.reset_index(inplace=True)
        self.wallet_data.df = filtered_data
