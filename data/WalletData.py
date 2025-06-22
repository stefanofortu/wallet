import pandas as pd
import logging

logger = logging.getLogger("Stefano")


class WalletData:
    def __init__(self, data):
        self.data_columns = ['account', 'category', 'amount', 'type', 'note', 'date', 'labels']

        if not isinstance(data, pd.DataFrame):
            logger.error("WalletData - init(): Wrong input type for data")
            raise TypeError

        self.data = data
        self.verify_currency()
        self.filter_out_columns()
        self.select_personal_accounts()

        mask_loan_debts = self.data['category'].isin(['Credito', 'Prestito', "Refunds"])
        self.df_loan_debts = self.data[mask_loan_debts]

        mask_transfer = (self.data['category'] == 'TRANSFER')
        self.df_transfers = self.data[mask_transfer]

        mask_contabile = (self.data['category'] == 'Contabile')
        self.df_contabile = self.data[mask_contabile]

        self.not_main = self.data[(mask_loan_debts | mask_transfer | mask_contabile)]
        self.df_main = self.data[~(mask_loan_debts | mask_transfer | mask_contabile)]

    def verify_currency(self):
        currency_list = self.data['currency'].unique()
        if currency_list.size != 1 or currency_list[0] != 'EUR':
            raise ValueError('All currency in dataframe are not EURO (€)')

    def filter_out_columns(self):
        self.data.drop(columns=['ref_currency_amount', 'payment_type', 'payment_type_local',
                              'gps_latitude', 'gps_longitude', 'gps_accuracy_in_meters',
                              'warranty_in_month', 'transfer', 'payee', "currency",
                              'envelope_id', 'custom_category'], inplace=True)
        self.data.reset_index(inplace=True, drop=True)

        column_list = list(self.data.columns)
        difference_column_list = list(set(self.data_columns) ^ set(column_list))

        if len(difference_column_list) > 0:
            logger.error("more column than allowed in import file")
            raise ImportError

    def select_personal_accounts(self):
        all_accounts = self.data['account'].unique()
        accounts_to_keep = list(["Cash", "Carta", "Banca", "Poste", "Barclays", "BPM"])
        account_to_be_removed = list(set(all_accounts) - set(accounts_to_keep))
        for account in account_to_be_removed:
            self.data = self.data.drop(
                self.data[self.data["account"] == account].index)
        self.data.reset_index(inplace=True, drop=True)

        accounts = list(self.data['account'].unique())
        account_remained = list(set(accounts) ^ set(accounts_to_keep))
        if len(account_remained) > 0:
            logger.info("The following accounts are not present" + str(account_remained))