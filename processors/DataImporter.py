import pandas as pd
import math
from data.WalletData import WalletData
import logging

logger = logging.getLogger("Stefano")


class DataImporter:

    def __init__(self, filename, main_wallet_selection=True, start_date=None, end_date=None, ):
        self.input_filename = filename
        self.wallet_data = None
        self.start_date = start_date
        self.end_date = end_date

        self.import_file(main_wallet_selection=main_wallet_selection)
        # only on df_main and not in df_transfers
        self.filter_data_by_time()
        self.verify_single_label()
        self.verify_single_label_for_transfers()
        # self.find_transfers_inside_outside_wallet()
        self.verify_single_label_loan_debts()
        self.verify_single_label_contabile()

    def get_imported_data(self) -> WalletData:
        return self.wallet_data

    def import_file(self, main_wallet_selection):
        all_data = pd.read_excel(self.input_filename)
        self.wallet_data = WalletData(all_data, main_wallet_selection)
        del all_data



    def verify_single_label(self):
        labels_imported = self.wallet_data.df_main['labels'].unique()
        self.wallet_data.df_main.to_csv('debug.csv')
        wrong_label = False
        empty_label = False
        for label in labels_imported:
            if isinstance(label, str):
                if label != "in" and label != "out" and label != "risparmi":
                    wrong_label = True
            else:
                if math.isnan(label):  # (labels_imported.isna()).any(axis=None):
                    empty_label = True

        if empty_label or wrong_label:
            logger.info("all labels imported:" + str(labels_imported))
            filtered_data = self.wallet_data.df_main[(self.wallet_data.df_main["labels"] != "in") &
                                                     (self.wallet_data.df_main["labels"] != "out") &
                                                     (self.wallet_data.df_main["labels"] != "risparmi")]
            logger.info(filtered_data[['date', 'account', 'category', 'labels']])
            if wrong_label:
                raise ValueError('verify_single_label(). Label not in/out/savings')
            if empty_label:
                raise ValueError('verify_single_label(). Label empty')

    def verify_single_label_for_transfers(self):
        labels_imported = self.wallet_data.df_transfers['labels'].unique()
        # logger.info("all labels imported:" + str(labels_imported))
        df_noNan = self.wallet_data.df_transfers.dropna(subset=['labels'])
        labels_imported_noNan = df_noNan['labels'].unique()
        # logger.info("labels_imported_noNan:" + str(labels_imported_noNan))

        wrong_label = False
        empty_label = False
        for label in labels_imported_noNan:
            if isinstance(label, str):
                if label != "In_Casa_Stefano" and label != "In_Casa_Severo" and label != "contabile":
                    wrong_label = True

        if wrong_label:
            # logger.info("all labels imported:" + str(labels_imported_noNan))
            filtered_data = df_noNan[(df_noNan["labels"] != "In_Casa_Stefano") &
                                     (df_noNan["labels"] != "In_Casa_Severo") &
                                     (df_noNan["labels"] != "contabile")]
            # logger.info(filtered_data[['date', 'account', 'category', 'labels']])
            if wrong_label:
                raise ValueError('verify_single_label(). Label not In_Casa_Stefano/In_Casa_Severo/contabile')
            if empty_label:
                raise ValueError('verify_single_label(). Label empty')

        # if wrong_label:
        #    print("all labels found in TRANSFERS:" + str(labels_imported))
        #    df_no_nan = self.wallet_data.df_transfers.dropna(subset=['labels'])
        #    filtered_data = df_no_nan[(df_no_nan["labels"] != "contabile")]
        #    logger.info(filtered_data[['date', 'account', 'category', 'labels']])
        #    raise ValueError('verify_single_label_for_transfers(). Label not \'contabile\'')

    def verify_single_label_loan_debts(self):
        # labels_imported = self.wallet_data.df_loan_debts['labels'].unique()
        # logger.info("all labels imported:" + str(labels_imported))
        df_no_nan = self.wallet_data.df_loan_debts.dropna(subset=['labels'])
        labels_imported_no_nan = df_no_nan['labels'].unique()

        if len(labels_imported_no_nan) > 0:
            logger.info("verify_single_label_loan_debts(): labels_imported_noNan:" + str(labels_imported_no_nan))
            print(df_no_nan)
            raise ValueError('verify_single_label_loan_debts(). Tag not empty')

    def verify_single_label_contabile(self):
        # labels_imported = self.wallet_data.df_loan_debts['labels'].unique()
        # logger.info("all labels imported:" + str(labels_imported))
        df_no_nan = self.wallet_data.df_contabile.dropna(subset=['labels'])
        labels_imported_no_nan = df_no_nan['labels'].unique()

        if len(labels_imported_no_nan) > 0:
            logger.info("verify_single_label_contabile(): labels_imported_noNan:" + str(labels_imported_no_nan))
            print(df_no_nan)
            raise ValueError('verify_single_label_contabile(). Tag not empty')

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

        filtered_data = self.wallet_data.df_main[(self.wallet_data.df_main["date"] >= timestamp_start_date) &
                                                 (self.wallet_data.df_main["date"] <= timestamp_end_date)]
        filtered_data.reset_index(inplace=True)
        self.wallet_data.df_main = filtered_data

    def find_transfers_inside_outside_wallet(self):

        # Conta quante volte ciascun trasferimento ha uan specifica data
        conteggio = self.wallet_data.df_transfers['date'].value_counts()
        # print(self.wallet_data.df_transfers[["account", "category", "amount", "type", "date", "labels"]].to_string(
        #    index=False))
        # Seleziona i valori che compaiono esattamente due volte
        valori_con_due_occorrenze = conteggio[conteggio == 2].index

        # Filtra il DataFrame escludendo le righe che hanno doppia quei valori in 'A'
        df_transfers_doppi = self.wallet_data.df_transfers[
            self.wallet_data.df_transfers['date'].isin(valori_con_due_occorrenze)]
        df_senza_transfers_doppi = self.wallet_data.df_transfers[
            ~self.wallet_data.df_transfers['date'].isin(valori_con_due_occorrenze)]

        df_transfers_doppi_per_anno = df_transfers_doppi[df_transfers_doppi['date'].dt.year == 2024]
        # print(df_transfers_doppi_per_anno)
        # Somma della colonna 'B'
        somma_df_transfers_doppi = df_transfers_doppi_per_anno['amount'].sum()
        print("Somma colonna importi df_transfers_doppi:", somma_df_transfers_doppi)

        df_transfers_non_doppi_per_anno = df_senza_transfers_doppi[df_senza_transfers_doppi['date'].dt.year == 2023]

        print(df_transfers_non_doppi_per_anno[["account", "category", "amount", "type", "date", "labels"]].to_string(
            index=False))
        somma_df_senza_transfers_doppi = df_senza_transfers_doppi['amount'].sum()
        print("Somma colonna importi df_transfers non doppi:", somma_df_senza_transfers_doppi)
