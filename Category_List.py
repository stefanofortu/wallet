class AllCategory:
    def __init__(self):
        self.all_category = []
        self.init_all_category()

    def init_all_category(self):
        self.all_category.extend(
            ["Cibo & Bevande", "Bar & Locali", "Lunch", "Spesa",
             "Shopping", "Abbigliamento & Scarpe","Electronics", "Gifts",
             "Home", "Affitto/Mutuo", "Energia, Utenze", "Family",
             "Furniture, Maintenance", "Trasporti", "Trasporto pubblico",
             "Veicoli", "Assicurazione veicoli", "Carburante", "Manutenzione veicoli", "Parking and Tolls",
             "Entertainment", "Eventi", "Fun", "Hobby", "Personal Care", "Sport, fitness",
             "Travel & Holidays","Summer Holidays", "Weekends",
             "Spese finanziarie", "Beneficienza", "Salute",
             "Investimenti", "Education", "Work", "Beni immobili", "Education_New", "Work_New",
             "Introiti", "Entrate da affitto", "Interessi, Dividendi", "Refunds", "Salary",
             "Altro", "Correzioni", "Prelievo", "Trasferimento", "Correzioni",
             "Prelievo", "Trasferimento", "Salary IN", "Salary OUT", "Unexpected", "Placeholder"])


class Main_Category(AllCategory):
    def __init__(self):

        self.category = []
        self.init_all_category()

    def init_all_category(self):
        self.all_category.extend(
            ["Cibo & Bevande", "Bar & Locali", "Lunch", "Spesa",
             "Shopping", "Abbigliamento & Scarpe","Electronics", "Gifts",
             "Home", "Affitto/Mutuo", "Energia, Utenze", "Family",
             "Furniture, Maintenance", "Trasporti", "Trasporto pubblico",
             "Veicoli", "Assicurazione veicoli", "Carburante", "Manutenzione veicoli", "Parking and Tolls",
             "Entertainment", "Eventi", "Fun", "Hobby", "Personal Care", "Sport, fitness",
             "Travel & Holidays","Summer Holidays", "Weekends",
             "Spese finanziarie", "Beneficienza", "Salute",
             "Investimenti", "Education", "Work", "Beni immobili", "Education_New", "Work_New",
             "Introiti", "Entrate da affitto", "Interessi, Dividendi", "Refunds", "Salary",
             "Altro", "Correzioni", "Prelievo", "Trasferimento", "Correzioni",
             "Prelievo", "Trasferimento", "Salary IN", "Salary OUT", "Unexpected", "Placeholder"])

class CategoryResults:
    def __init__(self):
        self.results = {}

    def __str__(self):
        output_str = ""
        for k in self.results.keys():
            output_str += str(k) + ": " + str(self.results[k]) + "\n"
        return output_str

    def append(self, category, amount):
        self.results[category] = amount
