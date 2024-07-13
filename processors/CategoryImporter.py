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

        category_results = CategoryResults()
        for category in self.all_category:
            filtered_data_in = data.df[(data.df["category"] == category) & (data.df["labels"] == "in")]
            filtered_data_in.reset_index(inplace=True)
            amount_in = filtered_data_in['amount'].sum()

            filtered_data_out = data.df[(data.df["category"] == category) & (data.df["labels"] == "out")]
            filtered_data_out.reset_index(inplace=True)
            amount_out = filtered_data_out['amount'].sum()

            filtered_data_savings = data.df[(data.df["category"] == category) & (data.df["labels"] == "savings")]
            filtered_data_savings.reset_index(inplace=True)
            amount_savings = filtered_data_savings['amount'].sum()
            category_results.append(category, amount_in, amount_out, amount_savings)

        return category_results

    """ check_categories_name
        Funzione che controlla che le categorie in ingresso non abbiano nomi diversi da quelli previsti nella lista
    """

    def check_categories_name(self, data):
        categories_in_df = (list(data.df["category"].unique()))
        categories_excess = list(set(categories_in_df) - set(self.all_category))
        if len(categories_excess) > 0:
            print("CategoryImport.check_categories_name() - more categories in import file, ", categories_excess)
            raise TypeError
