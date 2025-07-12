from data.CategoryResults import CategoryResults
from data.CategoryStructure import CategoryStructure
from data.WalletData import WalletData
import logging

logger = logging.getLogger("Stefano")


class CategoryImporter:
    def __init__(self):
        self.all_category = CategoryStructure.get_basic_categories()
        logger.warning("Aggiungere due ulteriori gruppi: IN, Income_risparmi, Out, Expense_risparmi. Da gestire "
                       "correttamente")

    def process(self, data):
        if not isinstance(data, WalletData):
            logger.error("get_data_by_category(): Wrong input type for data")
            raise TypeError("get_data_by_category(): Wrong input type for data")

        self.verify_to_del_categories(data)
        self.check_all_labels_sign(data=data, label="in", sign="positive")
        self.check_all_labels_sign(data=data, label="out", sign="negative")
        self.check_all_category_sign(data=data, sign="positive")
        self.check_all_category_sign(data=data, sign="negative")

        data.df_main.amount = data.df_main.amount.round(2)
        category_results = CategoryResults()
        for category in self.all_category:
            filtered_data_in = data.df_main[(data.df_main["category"] == category) & (data.df_main["labels"] == "in")]
            filtered_data_in.reset_index(inplace=True)
            amount_in = round(filtered_data_in['amount'].sum(), 2)

            filtered_data_out = data.df_main[(data.df_main["category"] == category) & (data.df_main["labels"] == "out")]
            filtered_data_out.reset_index(inplace=True)
            amount_out = round(filtered_data_out['amount'].sum(), 2)

            filtered_data_savings = data.df_main[(data.df_main["category"] == category) & (data.df_main["labels"] == "risparmi")]
            filtered_data_savings.reset_index(inplace=True)
            amount_savings = round(filtered_data_savings['amount'].sum(), 2)

            if amount_savings >= 0:
                amount_savings_in = amount_savings
                amount_savings_out = 0
            else:
                amount_savings_in = 0
                amount_savings_out = amount_savings

            category_results.append(category,
                                    amount_in=amount_in, amount_savings_in=amount_savings_in,
                                    amount_out=amount_out, amount_savings_out=amount_savings_out)
        return category_results

    """ check_categories_name
        Funzione che controlla che le categorie in ingresso non abbiano nomi diversi da quelli previsti nella lista
    """

    def verify_to_del_categories(self, data):
        category_to_del = CategoryStructure.get_expense_to_del()
        filtered_data = data.df_main.loc[data.df_main['category'].isin(category_to_del) & data.df_main['amount'] != 0]
        filtered_data.reset_index(inplace=True, drop=True)
        if filtered_data.size > 0:
            logger.error("Some of the expenses that should be zero are populated")
            print(filtered_data[["date", "account", "category", "amount", "labels"]])

    def check_all_labels_sign(self, data, label, sign):
        if not isinstance(data, WalletData):
            logger.error("check_all_labels_are_positive(): Wrong input type for data")
            raise TypeError("check_all_labels_are_positive(): Wrong input type for data")
        if sign == "positive":
            df_results = data.df_main.loc[(data.df_main["labels"] == label) &
                                     (data.df_main["amount"] < 0),
                                     ["date", "account", "amount"]]  # == label ]).loc[:, ["amount"]] < 0
        elif sign == "negative":
            df_results = data.df_main.loc[(data.df_main["labels"] == label) &
                                     (data.df_main["amount"] > 0),
                                     ["date", "account", "amount"]]
        else:
            raise TypeError("CategoryImporter.check_all_labels_value() - sign parameters incorrect",
                            sign)

        if not df_results.empty:
            logger.error("Found transactions where label %s is not %s" % (label, sign))
            print(df_results)

    @staticmethod
    def check_all_category_sign(data, sign):
        if not isinstance(data, WalletData):
            logger.error("check_all_category_sign(): Wrong input type for data")
            raise TypeError("check_all_category_sign(): Wrong input type for data")

        if sign == "positive":
            category_list = CategoryStructure.get_income_categories()
            df_results = data.df_main.loc[(data.df_main["category"].isin(category_list)) &
                                     (data.df_main["amount"] < 0),
                                     ["date", "account", "amount"]]
        elif sign == "negative":
            category_list = CategoryStructure.get_expense_categories()

            df_results = data.df_main.loc[(data.df_main["category"].isin(category_list)) &
                                     (data.df_main["amount"] > 0),
                                     ["date", "account", "amount"]]
        else:
            raise TypeError("CategoryImporter.check_all_category_sign() - sign parameters incorrect",
                            sign)

        if not df_results.empty:
            logger.error("Found transactions where category is not %s" % sign)
            print(df_results)
