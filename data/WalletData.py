import pandas as pd
import logging
from data.CategoryStructure import CategoryStructure

logger = logging.getLogger("Stefano")


class WalletData:
    def __init__(self, data, main_wallet_selection):
        self.data_columns = ['account', 'category', 'amount', 'type', 'note', 'date', 'labels']

        if not isinstance(data, pd.DataFrame):
            logger.error("WalletData - init(): Wrong input type for data")
            raise TypeError

        self.all_data = data
        self.verify_currency()
        self.filter_out_columns()
        if main_wallet_selection:
            self.select_personal_accounts()
        else:
            self.select_home_accounts()
        self.check_categories_name()

        mask_loan_debts = self.all_data['category'].isin(['Credito', 'Prestito', "Refunds", "Restituzione credito"])
        self.df_loan_debts = self.all_data[mask_loan_debts]

        mask_transfer = (self.all_data['category'] == 'TRANSFER')
        self.df_transfers = self.all_data[mask_transfer]

        mask_contabile = (self.all_data['category'] == 'Contabile')
        self.df_contabile = self.all_data[mask_contabile]

        self.not_main = self.all_data[(mask_loan_debts | mask_transfer | mask_contabile)]
        self.df_main = self.all_data[~(mask_loan_debts | mask_transfer | mask_contabile)]

    def verify_currency(self):
        currency_list = self.all_data['currency'].unique()
        if currency_list.size != 1 or currency_list[0] != 'EUR':
            raise ValueError('All currency in dataframe are not EURO (€)')

    def filter_out_columns(self):
        self.all_data.drop(columns=['ref_currency_amount', 'payment_type', 'payment_type_local',
                                'gps_latitude', 'gps_longitude', 'gps_accuracy_in_meters',
                                'warranty_in_month', 'transfer', 'payee', "currency",
                                'envelope_id', 'custom_category'], inplace=True)
        self.all_data.reset_index(inplace=True, drop=True)

        column_list = list(self.all_data.columns)
        difference_column_list = list(set(self.data_columns) ^ set(column_list))

        if len(difference_column_list) > 0:
            logger.error("more column than allowed in import file")
            raise ImportError

    def select_personal_accounts(self):
        all_accounts = self.all_data['account'].unique()
        accounts_to_keep = list(["Cash", "Carta", "Banca", "Poste", "Barclays", "BPM"])
        account_to_be_removed = list(set(all_accounts) - set(accounts_to_keep))
        for account in account_to_be_removed:
            self.all_data = self.all_data.drop(
                self.all_data[self.all_data["account"] == account].index)
        self.all_data.reset_index(inplace=True, drop=True)

        accounts = list(self.all_data['account'].unique())
        account_remained = list(set(accounts) ^ set(accounts_to_keep))
        if len(account_remained) > 0:
            logger.info("The following accounts are not present" + str(account_remained))

    def select_home_accounts(self):
        all_accounts = self.all_data['account'].unique()
        accounts_to_keep = list(["Cash Casa"])
        account_to_be_removed = list(set(all_accounts) - set(accounts_to_keep))
        for account in account_to_be_removed:
            self.all_data = self.all_data.drop(
                self.all_data[self.all_data["account"] == account].index)
        self.all_data.reset_index(inplace=True, drop=True)

        accounts = list(self.all_data['account'].unique())
        account_remained = list(set(accounts) ^ set(accounts_to_keep))
        if len(account_remained) > 0:
            logger.info("The following accounts are not present" + str(account_remained))

    def check_categories_name(self):
        all_category = CategoryStructure.get_basic_categories()
        categories_in_df = (list(self.all_data["category"].unique()))
        categories_excess = list(set(categories_in_df) - set(all_category))
        if len(categories_excess) > 0:
            raise TypeError("WalletData.check_categories_name() - more categories in import file, ",
                            categories_excess)