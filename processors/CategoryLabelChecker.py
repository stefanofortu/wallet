import pandas
from data.CategoryStructure import CategoryStructure
from data.ExpenseGroups import ExpenseGroups
from data.WalletData import WalletData
import logging
from utils.LoggingStream import df_logger

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
        self.verify_single_labels(dataframe=df_contabile, labels_list=[], marker="df_contabile")
        self.verify_single_labels(dataframe=df_salary_in_out, labels_list=[], marker="df_salary_in_out")

        if self.main_wallet_selection:
            self.verify_single_labels(dataframe=df_main, labels_list=["in", "out", "risparmi"],
                                      marker="df_main_wallet")
        else:
            self.verify_single_labels(dataframe=df_main, labels_list=["in","In_Casa_Stefano", "Out_Casa", "In_Casa_Severo"],
                                      marker="df_main_home")
            data.all_data['labels'] = data.all_data['labels'].replace({'In_Casa_Stefano': 'in',
                                                                     'Out_Casa': 'out',
                                                                     'In_Casa_Severo': 'in'})

        data.all_data['labels'] = data.all_data['labels'].replace('contabile', 'no_tags')
        data.all_data['labels'] = data.all_data['labels'].fillna('no_tags')
        data.all_data['labels'] = data.all_data['labels'].replace('', 'no_tags')

        self.verify_single_labels(dataframe=data.all_data, labels_list=["in", "out", "risparmi", "no_tags"])

        self.check_all_labels_sign(data=data, label="in", sign="positive")
        self.check_all_labels_sign(data=data, label="out", sign="negative")

        self.find_transfers_inside_outside_wallet(df_transfers)

        return True

    @staticmethod
    def check_categories_name(data):
        all_category = CategoryStructure.get_basic_categories()
        categories_in_df = (list(data.all_data["category"].unique()))
        categories_excess = list(set(categories_in_df) - set(all_category))
        if len(categories_excess) > 0:
            logger.error(f"WalletData.check_categories_name() - more categories in import file : {categories_excess}")
            for cat in categories_excess:
                df_to_print = data.all_data[data.all_data['category'] == cat]
                df_logger.print_df(df_to_print, category=True, note=True)

        logger.info("Checking no other categories than allowed in import file: DONE")

    @staticmethod
    def check_all_category_sign(data, sign):
        if not isinstance(data, WalletData):
            logger.error("check_all_category_sign(): Wrong input type for data")
            raise TypeError("check_all_category_sign(): Wrong input type for data")

        if sign == "positive":
            category_list = ExpenseGroups.get_income_categories()
            df_results = data.all_data.loc[(data.all_data["category"].isin(category_list)) &
                                           (data.all_data["amount"] < 0), :]
        elif sign == "negative":
            category_list = ExpenseGroups.get_expense_categories()

            df_results = data.all_data.loc[(data.all_data["category"].isin(category_list)) &
                                           (data.all_data["amount"] > 0), :]
        else:
            raise TypeError("CategoryImporter.check_all_category_sign() - sign parameters incorrect",
                            sign)

        if not df_results.empty:
            logger.error("Found transactions where category is not %s" % sign)
            df_logger.print_df(dataframe=df_results, category=True, note=True, amount=True)

    @staticmethod
    def verify_to_del_categories(data):
        category_to_del = ExpenseGroups.get_expense_to_del()
        filtered_data = data.all_data.loc[data.all_data['category'].isin(category_to_del) &
                                          data.all_data['amount'] != 0]
        filtered_data.reset_index(inplace=True, drop=True)
        if filtered_data.size > 0:
            logger.error("Some of the expenses that should be zero are populated")
            df_logger.print_df(dataframe=filtered_data, category=True, note=True, amount=True)

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
                logger.error(f"wrong_label_list :" + str(wrong_label_list))
                df_logger.print_df(df_no_nan, note=True, labels=True, category=True, amount=True)

        if values_acceptable == "Not Nan" or values_acceptable == "mixed":
            if len(wrong_label_list) > 0:
                logger.error(f"verify_single_labels() for {marker}. Label not in input list {wrong_label_list}")
                df_logger.print_df(df_wrong_label, note=True, labels=True, category=True, amount=True)

        if values_acceptable == "Not Nan":
            if not df_nan.empty:
                logger.error(f"verify_single_labels() for {marker}. Nan label present")
                df_logger.print_df(df_nan, note=True, labels=True, category=True, amount=True)
        # logger.info(f"marker end : {marker}")

    @staticmethod
    def check_all_labels_sign(data, label, sign):
        if not isinstance(data, WalletData):
            logger.error("check_all_labels_are_positive(): Wrong input type for data")
            raise TypeError("check_all_labels_are_positive(): Wrong input type for data")
        if sign == "positive":
            df_results = data.all_data.loc[(data.all_data["labels"] == label) &
                                           (data.all_data["amount"] < 0), :]
        elif sign == "negative":
            df_results = data.all_data.loc[(data.all_data["labels"] == label) &
                                           (data.all_data["amount"] > 0), :]
        else:
            raise TypeError("CategoryImporter.check_all_labels_value() - sign parameters incorrect",
                            sign)

        if not df_results.empty:
            logger.error("Found transactions where label %s is not %s" % (label, sign))
            df_logger.print_df(df_results, category=True, note=True, labels=True, amount=True)

    @staticmethod
    def find_transfers_inside_outside_wallet(df_transfers):
        logger.info("Checking the transfers inside/outside of the wallet")
        # Conta quante volte ciascun trasferimento ha una specifica data
        conteggio = df_transfers['date'].value_counts()

        # Seleziona i valori che compaiono esattamente due volte
        valori_con_due_occorrenze = conteggio[conteggio == 2].index

        # Filtra il DataFrame escludendo le righe che hanno doppia quei valori in 'A'
        df_transfers_doppi = df_transfers[
            df_transfers['date'].isin(valori_con_due_occorrenze)]
        df_senza_transfers_doppi = df_transfers[
            ~df_transfers['date'].isin(valori_con_due_occorrenze)]

        somma_df_transfers_doppi = round(df_transfers_doppi['amount'].sum(), 2)
        logger.info(f"Somma colonna importi CON df_transfers_doppi: {somma_df_transfers_doppi}")
        if not df_senza_transfers_doppi.empty:
            logger.info(f"Stampo i dataframe dove non ci sono date con due occorrenze")
            df_logger.print_df(df_senza_transfers_doppi,
                                amount=True, category=True, note=True, labels=False)
        somma_df_senza_transfers_doppi = round(df_senza_transfers_doppi['amount'].sum(), 2)
        logger.info(f"Somma colonna importi df_transfers_doppi: {somma_df_senza_transfers_doppi}")

        logger.info("Checking double transfers: DONE")