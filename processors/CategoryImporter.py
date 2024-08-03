from data.CategoryResults import CategoryResults
from data.CategoryStructure import CategoryStructure
from data.WalletData import WalletData


class CategoryImporter:
    def __init__(self):
        self.all_category = CategoryStructure.get_basic_categories()

    def process(self, data):
        if not isinstance(data, WalletData):
            print("get_data_by_category(): Wrong input type for data")
            raise TypeError("get_data_by_category(): Wrong input type for data")

        self.check_categories_name(data)
        self.verify_to_del_categories(data)

        data.df.amount = data.df.amount.round(2)
        category_results = CategoryResults()
        for category in self.all_category:
            filtered_data_in = data.df[(data.df["category"] == category) & (data.df["labels"] == "in")]
            filtered_data_in.reset_index(inplace=True)
            amount_in = round(filtered_data_in['amount'].sum(), 2)

            filtered_data_out = data.df[(data.df["category"] == category) & (data.df["labels"] == "out")]
            filtered_data_out.reset_index(inplace=True)
            amount_out = round(filtered_data_out['amount'].sum(), 2)

            filtered_data_savings = data.df[(data.df["category"] == category) & (data.df["labels"] == "risparmi")]
            filtered_data_savings.reset_index(inplace=True)
            amount_savings = round(filtered_data_savings['amount'].sum(), 2)

            category_results.append(category, amount_in, amount_out, amount_savings)

        return category_results

    """ check_categories_name
        Funzione che controlla che le categorie in ingresso non abbiano nomi diversi da quelli previsti nella lista
    """

    def check_categories_name(self, data):
        categories_in_df = (list(data.df["category"].unique()))
        categories_excess = list(set(categories_in_df) - set(self.all_category))
        if len(categories_excess) > 0:
            raise TypeError("CategoryImport.check_categories_name() - more categories in import file, ",
                            categories_excess)

    def verify_to_del_categories(self, data):
        category_to_del = CategoryStructure.get_expense_to_del()
        filtered_data = data.df.loc[data.df['category'].isin(category_to_del) & data.df['amount'] != 0]
        filtered_data.reset_index(inplace=True, drop=True)
        if filtered_data.size > 0:
            print("Some of the expenses that should be zero are populated")
            print(filtered_data[["date", "account", "category", "amount", "labels"]])
            exit()
