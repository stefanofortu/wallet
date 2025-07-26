import logging
logger = logging.getLogger("Stefano")


class CategoryStructure:
    categories = {"Cibo & Bevande": ["Bar & Locali", "Lunch", "Spesa"],
                  "Shopping": ["Abbigliamento & Scarpe", "Electronics", "Gifts"],
                  "Home": ["Affitto/Mutuo", "Energia & Utenze", "Family", "Furniture, Maintenance"],
                  "Trasporti": ["Trasporto pubblico"],
                  "Veicoli": ["Assicurazione veicoli", "Carburante", "Manutenzione veicoli", "Parking and Tolls"],
                  "Entertainment": ["Eventi", "Fun", "Hobby", "Personal Care",
                                    "Sport & Fitness"],  # , "Summer Holidays", "Weekends"],
                  "Travel & Holidays": ["Summer Holidays", "Weekends"],
                  "Spese finanziarie": ["Beneficienza", "Salute", "Prestito", "Restituzione credito"],
                  "Investimenti": ["Education", "Work", "Beni immobili", "Education_New", "Work_New"],
                  "Introiti": ["Entrate da affitto", "Interessi & Dividendi", "Refunds", "Salary", "Regali", "Credito",
                               "Quote"],
                  "Altro": ["Prelievo", "Correzioni", "TRANSFER", "Salary IN", "Salary OUT", "Unexpected",
                            "Placeholder", "Adjust balance", "Check Balance", "Contabile"]
                  }

    @staticmethod
    def get_category_structure():
        return CategoryStructure.categories

    @staticmethod
    def get_basic_categories():
        category_list = []
        for c in CategoryStructure.categories.keys():
            category_list.extend(CategoryStructure.categories[c])

        return category_list
