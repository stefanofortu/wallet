import math

import pandas

from data.CategoryStructure import CategoryStructure
from data.ExpenseGroups import ExpenseGroups
from data.WalletData import WalletData
import logging

logger = logging.getLogger("Stefano")


class CategoryLabelChecker:
    def __init__(self, main_wallet_selection):
        self.main_wallet_selection = main_wallet_selection

    def process(self, data):
        if not isinstance(data, WalletData):
            logger.error("get_data_by_category(): Wrong input type for data")
            raise TypeError("get_data_by_category(): Wrong input type for data")

        self.check_categories_name(data=data)
        self.check_all_category_sign(data=data, sign="positive")
        self.check_all_category_sign(data=data, sign="negative")
        self.verify_to_del_categories(data=data)

        mask_loan_debts = data.all_data['category'].isin(
            ['Credito', 'Prestito', "Refunds", "Restituzione credito"])
        df_loan_debts = data.all_data[mask_loan_debts]

        mask_transfer = (data.all_data['category'] == 'TRANSFER')
        df_transfers = data.all_data[mask_transfer]

        mask_contabile = (data.all_data['category'] == 'Contabile')
        df_contabile = data.all_data[mask_contabile]

        mask_salary_in_out = data.all_data['category'].isin(['Salary IN', 'Salary OUT'])
        df_salary_in_out = data.all_data[mask_salary_in_out]

        df_main = data.all_data[~(mask_loan_debts | mask_transfer | mask_contabile | mask_salary_in_out)]
        df_not_main = data.all_data[(mask_loan_debts | mask_transfer | mask_contabile | mask_salary_in_out)]

        if self.main_wallet_selection and not df_salary_in_out.empty:
            logger.error("Main wallet selected but Salary IN/OUT transitions present")

        self.verify_single_labels(dataframe=df_loan_debts, labels_list=[], marker="df_loan_debts")
        self.verify_single_labels(dataframe=df_transfers, labels_list=[], marker="df_transfers")
        self.verify_single_labels(dataframe=df_contabile, labels_list=["contabile"], marker="df_contabile")
        self.verify_single_labels(dataframe=df_salary_in_out, labels_list=[], marker="df_salary_in_out")

        if self.main_wallet_selection:
            self.verify_single_labels(dataframe=df_main, labels_list=["in", "out", "risparmi"],
                                      marker="df_main_wallet")
        else:
            self.verify_single_labels(dataframe=df_main, labels_list=["In_Casa_Stefano", "Out_Casa", "In_Casa_Severo"],
                                      marker="df_main_home")
            data.df_main['labels'] = data.df_main['labels'].replace({'In_Casa_Stefano': 'in',
                                                                     'Out_Casa': 'out',
                                                                     'In_Casa_Severo': 'in'})

        data.all_data['labels'] = data.all_data['labels'].replace('contabile', 'no_tags')
        data.all_data['labels'] = data.all_data['labels'].fillna('no_tags')
        data.all_data['labels'] = data.all_data['labels'].replace('', 'no_tags')

        self.verify_single_labels(dataframe=data.all_data, labels_list=["in", "out", "risparmi", "no_tags"])

        return True
        # only on df_main and not in df_transfers

        self.verify_single_label_for_transfers()
        # self.find_transfers_inside_outside_wallet()
        self.verify_single_label_loan_debts()
        self.verify_single_label_contabile()

        self.check_all_labels_sign(data=data, label="in", sign="positive")
        self.check_all_labels_sign(data=data, label="out", sign="negative")
        return True

    @staticmethod
    def check_all_category_sign(data, sign):
        if not isinstance(data, WalletData):
            logger.error("check_all_category_sign(): Wrong input type for data")
            raise TypeError("check_all_category_sign(): Wrong input type for data")

        if sign == "positive":
            category_list = ExpenseGroups.get_income_categories()
            df_results = data.all_data.loc[(data.all_data["category"].isin(category_list)) &
                                           (data.all_data["amount"] < 0),
                                           ["date", "account", "amount", "category"]]
        elif sign == "negative":
            category_list = ExpenseGroups.get_expense_categories()

            df_results = data.all_data.loc[(data.all_data["category"].isin(category_list)) &
                                           (data.all_data["amount"] > 0),
                                           ["date", "account", "amount", "category"]]
        else:
            raise TypeError("CategoryImporter.check_all_category_sign() - sign parameters incorrect",
                            sign)

        if not df_results.empty:
            logger.error("Found transactions where category is not %s" % sign)
            print(df_results)

    @staticmethod
    def verify_to_del_categories(data):
        category_to_del = ExpenseGroups.get_expense_to_del()
        filtered_data = data.all_data.loc[data.all_data['category'].isin(category_to_del) &
                                          data.all_data['amount'] != 0]
        filtered_data.reset_index(inplace=True, drop=True)
        if filtered_data.size > 0:
            logger.error("Some of the expenses that should be zero are populated")
            print(filtered_data[["date", "account", "category", "amount", "labels"]])

    @staticmethod
    def check_all_labels_sign(data, label, sign):
        if not isinstance(data, WalletData):
            logger.error("check_all_labels_are_positive(): Wrong input type for data")
            raise TypeError("check_all_labels_are_positive(): Wrong input type for data")
        if sign == "positive":
            df_results = data.all_data.loc[(data.all_data["labels"] == label) &
                                           (data.all_data["amount"] < 0),
                                           ["date", "account", "amount"]]  # == label ]).loc[:, ["amount"]] < 0
        elif sign == "negative":
            df_results = data.all_data.loc[(data.all_data["labels"] == label) &
                                           (data.all_data["amount"] > 0),
                                           ["date", "account", "amount"]]
        else:
            raise TypeError("CategoryImporter.check_all_labels_value() - sign parameters incorrect",
                            sign)

        if not df_results.empty:
            logger.error("Found transactions where label %s is not %s" % (label, sign))
            print(df_results)

    def verify_single_label_main_wallet(self, data):
        labels_imported = data.all_data['labels'].unique()
        wrong_label = False
        empty_label = False
        for label in labels_imported:
            if isinstance(label, str):
                if label != "in" and label != "out" and label != "risparmi" and label != "no_tags":
                    wrong_label = True
            else:
                if math.isnan(label):  # (labels_imported.isna()).any(axis=None):
                    empty_label = True

        if empty_label or wrong_label:
            logger.info("all labels imported:" + str(labels_imported))
            filtered_data = data.all_data[(data.all_data["labels"] != "in") &
                                          (data.all_data["labels"] != "out") &
                                          (data.all_data["labels"] != "risparmi") &
                                          (data.all_data["labels"] != "no_tags")]
            logger.info(filtered_data[['date', 'account', 'category', 'labels']])
            if wrong_label:
                raise ValueError('verify_single_label(). Label not in/out/savings/no_tags')
            if empty_label:
                raise ValueError('verify_single_label(). Label empty')

    def verify_single_label_home_wallet(self, data):
        labels_imported = data.all_data['labels'].unique()
        wrong_label = False
        empty_label = False
        for label in labels_imported:
            if isinstance(label, str):
                if label != "In_Casa_Stefano" and label != "Out_Casa" and label != "in" and label != "In_Casa_Severo":
                    wrong_label = True
            else:
                if math.isnan(label):  # (labels_imported.isna()).any(axis=None):
                    empty_label = True

        if empty_label or wrong_label:
            logger.info("all labels imported:" + str(labels_imported))
            filtered_data = data.all_data[(data.all_data["labels"] != "In_Casa_Stefano") &
                                          (data.all_data["labels"] != "In_Casa_Severo") &
                                          (data.all_data["labels"] != "in") &
                                          (data.all_data["labels"] != "Out_Casa")]

            logger.info(filtered_data[['date', 'account', 'category', 'labels']])
            if wrong_label:
                raise ValueError('verify_single_label(). Label not In_Casa_Stefano/Out_Casa/savings')
            if empty_label:
                raise ValueError('verify_single_label(). Label empty')

    def verify_single_label_for_transfers(self, data):
        labels_imported = data.df_transfers['labels'].unique()
        # logger.info("all labels imported:" + str(labels_imported))
        df_noNan = data.df_transfers.dropna(subset=['labels'])
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

    @staticmethod
    def verify_single_labels(dataframe, labels_list, marker=""):
        if not isinstance(dataframe, pandas.DataFrame):
            logger.error(f"verify_single_label for {marker}: dataframe input is not a pandas df ")
        if not isinstance(labels_list, list):
            logger.error(f"verify_single_label for {marker}: labels_list input is not a list")

        # logger.info(f"marker start : {marker}")
        if len(labels_list) == 0:
            values_acceptable = "NaN only"
            labels_list_no_nan = []
        elif len(labels_list) == 1:
            if None in labels_list:
                logger.error(f"verify_single_label for {marker}: only None value in labels_list")
                values_acceptable = "NaN only"
                labels_list_no_nan = []
            else:
                values_acceptable = "Not Nan"
                labels_list_no_nan = labels_list
        else:
            if None in labels_list:
                values_acceptable = "mixed"
                labels_list_no_nan = [x for x in labels_list if x is not None]
            else:
                values_acceptable = "Not Nan"
                labels_list_no_nan = labels_list

        # logger.info(f"values_acceptable: {values_acceptable}")

        df_nan = dataframe[dataframe['labels'].isna()]

        df_no_nan = dataframe.dropna(subset=['labels'])
        labels_imported_no_nan = df_no_nan['labels'].unique()
        wrong_label_list = []
        for label_read in labels_imported_no_nan:
            # logger.info(f"label_read : {label_read}")
            # logger.info(f"label_read type : {type(label_read)}")
            if isinstance(label_read, str):
                if label_read not in labels_list_no_nan:
                    wrong_label_list.append(label_read)
            df_wrong_label = dataframe[dataframe['labels'].isin(wrong_label_list)]

        if values_acceptable == "NaN only":
            if len(labels_imported_no_nan) > 0:
                logger.error(f"verify_single_labels() for {marker} - labels not empty:" + str(labels_imported_no_nan))
                logger.error(df_no_nan[['date', 'account', 'category', 'labels']])
                logger.error(f"wrong_label_list :" + str(wrong_label_list))


        if values_acceptable == "Not Nan" or values_acceptable == "mixed":
            if len(wrong_label_list) > 0:
                logger.error(f"verify_single_labels() for {marker}. Label not in input list {wrong_label_list}")
                logger.error(df_wrong_label[['date', 'account', 'category', 'labels']])

        if values_acceptable == "Not Nan":
            if not df_nan.empty:
                logger.error(f"verify_single_labels() for {marker}. Nan label present")
                logger.error(df_nan[['date', 'account', 'category', 'labels']])
        # logger.info(f"marker end : {marker}")

        return

        logger.info(f"labels_read : {labels_read}")
        logger.info(f"labels_len : {len(labels_read)}")
        wrong_label = False
        empty_label = False
        if labels is not None:
            for label_read in labels_read:
                logger.info(f"label_read : {label_read}")
                logger.info(f"label_read type : {type(label_read)}")
                if isinstance(label_read, str):
                    if label_read not in labels:
                        wrong_label = True
                        logger.info("label errata")
                    else:
                        if str(label_read).strip().lower() in ["nan", ""]:
                            empty_label = True
                            logger.info("label empty")
                        else:
                            logger.info("label ok")
                elif isinstance(label_read, float):
                    if math.isnan(label_read):
                        empty_label = True
                        logger.info("label Nan")

            if wrong_label:
                logger.info("all labels imported:" + str(labels_read))
                filtered_data = dataframe[dataframe['labels'].isin(labels)]
                logger.info(filtered_data[['date', 'account', 'category', 'labels']])
                if wrong_label:
                    raise ValueError(f'verify_single_labels() for {marker}. Label not in input list')
                if empty_label:
                    raise ValueError(f'verify_single_labels() for {marker}. Label empty')
            if empty_label:
                df_no_nan = dataframe.dropna(subset=['labels'])

    def verify_single_label_loan_debts(self):
        # labels_imported = self.wallet_data.df_loan_debts['labels'].unique()
        # logger.info("all labels imported:" + str(labels_imported))

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

    @staticmethod
    def check_categories_name(data):
        all_category = CategoryStructure.get_basic_categories()
        categories_in_df = (list(data.all_data["category"].unique()))
        categories_excess = list(set(categories_in_df) - set(all_category))
        if len(categories_excess) > 0:
            logger.error(f"WalletData.check_categories_name() - more categories in import file : {categories_excess}")

        logger.info("Checking no other categories than allowed in import file: DONE")

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
