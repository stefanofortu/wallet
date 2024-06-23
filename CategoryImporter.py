from CategoryResults import CategoryResults
from CategoryStructure import CategoryStructure
from WalletData import WalletData


class CategoryImporter:
    def __init__(self):
        self.all_category = ["Cibo & Bevande", "Bar & Locali", "Lunch", "Spesa",
                             "Shopping", "Abbigliamento & Scarpe", "Electronics", "Gifts",
                             "Home", "Affitto/Mutuo", "Energia & Utenze", "Family",
                             "Furniture, Maintenance", "Trasporti", "Trasporto pubblico",
                             "Veicoli", "Assicurazione veicoli", "Carburante", "Manutenzione veicoli",
                             "Parking and Tolls",
                             "Entertainment", "Eventi", "Fun", "Hobby", "Personal Care", "Sport & Fitness",
                             "Travel & Holidays", "Summer Holidays", "Weekends",
                             "Spese finanziarie", "Beneficienza", "Salute",
                             "Investimenti", "Education", "Work", "Beni immobili", "Education_New", "Work_New",
                             "Introiti", "Entrate da affitto", "Interessi, Dividendi", "Refunds", "Salary",
                             "Altro", "Correzioni", "Prelievo", "Trasferimento", "Correzioni", "Adjust balance",
                             "Prelievo", "Trasferimento", "Salary IN", "Salary OUT", "Unexpected", "Placeholder"]
        self.all_category = CategoryStructure.get_basic_categories()

    def process(self, data):
        if not isinstance(data, WalletData):
            print("get_data_by_category(): Wrong input type for data")
            raise TypeError

        self.check_categories_name(data)

        category_results = CategoryResults()
        for category in self.all_category:
            filtered_data = data.df[(data.df["category"] == category)]
            filtered_data.reset_index(inplace=True)
            amount = filtered_data['amount'].sum()
            category_results.append(category, amount)

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
