import pandas as pd


class WalletData:
    def __init__(self, data):
        self.data_columns = ['account', 'category', 'amount', 'type', 'note', 'date', 'labels']

        if not isinstance(data, pd.DataFrame):
            print("WalletData - init(): Wrong input type for data")
            raise TypeError

        self.df = data
        self.verify_currency()
        self.filter_out_columns()

    def verify_currency(self):
        a = self.df['currency'].unique()
        if a.size != 1 or a[0] != 'EUR':
            raise ValueError('All currency in dataframe are not EURO (€)')

    def filter_out_columns(self):
        self.df.drop(columns=['ref_currency_amount', 'payment_type', 'payment_type_local',
                              'gps_latitude', 'gps_longitude', 'gps_accuracy_in_meters',
                              'warranty_in_month', 'transfer', 'payee', "currency",
                              'envelope_id', 'custom_category'], inplace=True)
        self.df.reset_index(inplace=True, drop=True)

        column_list = list(self.df.columns)
        difference_column_list = list(set(self.data_columns) ^ set(column_list))

        if len(difference_column_list) > 0:
            print("more column than allowed in import file")
            raise ImportError
