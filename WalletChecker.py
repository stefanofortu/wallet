import numpy as np
import pandas as pd

class WalletChecker:
    def __init__(self):
        self.input_filename = "C:\\Users\\Stefano\\Documents\\MEGA\\MegaSync_Pixel\\report_2024-05-22_225645.xls"
        self.data = None
        self.import_file()
        self.filter_out_columns()

        # print(self.expense_handler.get_category_list())

    def import_file(self):
        self.data = pd.read_excel(self.input_filename)

    def filter_out_columns(self):
        # print(self.full_data.info())
        self.data.drop(columns=['ref_currency_amount', 'payment_type', 'payment_type_local',
                                'gps_latitude', 'gps_longitude', 'gps_accuracy_in_meters',
                                'warranty_in_month', 'transfer', 'payee',
                                'envelope_id', 'custom_category'], inplace=True)
        self.data.reset_index(inplace=True, drop=True)

        # print(self.full_data.info())
        # print("=====================================================================================", flush=True)

    def select_personal_accounts(self):
        all_accounts = self.data['account'].unique()
        accounts_to_keep = np.array(["Cash", "Carta", "Banca", "Poste", "Barclays"])
        account_to_be_removed = np.setdiff1d(all_accounts, accounts_to_keep)
        for account in account_to_be_removed:
            self.data = self.data.drop(self.data[self.data["account"] == account].index)
        self.data.reset_index(inplace=True, drop=True)

        accounts = self.data['account'].unique()
        if not ((accounts == accounts_to_keep).all()):
            print("Wallet_Checker::select_personal_accounts(): Error in account selection")
            return -1

    def get_category_list(self):
        if self.data is not None:
            return self.data['category'].unique()

    def get_data(self):
        return self.data

    @staticmethod
    def get_time_filtered_data(data, start_date, end_date):
        if not isinstance(data, pd.DataFrame):
            print("get_time_filtered_data(): Wrong input type for data")
            raise (TypeError)

        try:
            timestamp_start_date = pd.Timestamp(start_date)
        except:
            print("Error in timestamp_start_date()")
            raise (TypeError)
        try:
            timestamp_end_date = pd.Timestamp(end_date)
        except:
            print("Error in timestamp_end_date()")
            raise (TypeError)
        filtered_data = data[(data["date"] > timestamp_start_date) & (data["date"] < timestamp_end_date)]
        filtered_data.reset_index(inplace=True)
        return filtered_data

    @staticmethod
    def get_data_by_single_category(data, category):
        if not isinstance(data, pd.DataFrame):
            print("get_data_by_category(): Wrong input type for data")
            raise (TypeError)

        if not isinstance(category, str):
            print("get_data_by_category(): Wrong input type for category")
            raise (TypeError)

        filtered_data = data[(data["category"] == category)]
        filtered_data.reset_index(inplace=True)
        return filtered_data

    @staticmethod
    def get_amount_by_category(data, category):
        if not isinstance(data, pd.DataFrame):
            print("get_amount_by_category(): Wrong input type for data")
            raise (TypeError)

        if not isinstance(category, str):
            print("get_amount_by_category(): Wrong input type for category")
            raise (TypeError)

        try:
            dati_filtrati = WalletChecker.get_data_by_single_category(data=data, category=category)
        except  Exception as error:
            print("get_amount_by_category(): Wrong call to get_data_by_single_category", error)
            raise (TypeError)

        return round(dati_filtrati['amount'].sum())
