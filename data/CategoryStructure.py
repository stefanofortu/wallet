class CategoryStructure:
    categories = {"Cibo & Bevande": ["Bar & Locali", "Lunch", "Spesa"],
                  "Shopping": ["Abbigliamento & Scarpe", "Electronics", "Gifts"],
                  "Home": ["Affitto/Mutuo", "Energia & Utenze", "Family", "Furniture, Maintenance"],
                  "Trasporti": ["Trasporto pubblico"],
                  "Veicoli": ["Assicurazione veicoli", "Carburante", "Manutenzione veicoli", "Parking and Tolls"],
                  "Entertainment": ["Eventi", "Fun", "Hobby", "Personal Care",
                                    "Sport & Fitness", "Summer Holidays", "Weekends"],
                  "Travel & Holidays": ["Summer Holidays", "Weekends"],
                  "Spese finanziarie": ["Beneficienza", "Salute"],
                  "Investimenti": ["Education", "Work", "Beni immobili", "Education_New", "Work_New"],
                  "Introiti": ["Entrate da affitto", "Interessi & Dividendi", "Refunds", "Salary"],
                  "Altro": ["Correzioni", "Prelievo", "Trasferimento", "Correzioni",
                            "Trasferimento", "Salary IN", "Salary OUT", "Unexpected", "Placeholder", "Adjust balance",
                            "Check Balance"]
                  }

    expense_groups = {
        "Redditi": {
            "Income": ["Salary", "Interessi & Dividendi", "Refunds"]
        },
        "Essenziali_Dovute": {
            "Bollette_Manutenzione": ["Energia & Utenze", "Furniture, Maintenance", "Family"],
            "Macchina": ["Assicurazione veicoli", "Manutenzione veicoli"],
            "Salute_Beneficienza": ["Salute", "Beneficienza"]
        },
        "Indispensabili_Necessità": {
            "Spesa_Caffe_Lunch": ["Bar & Locali", "Lunch", "Spesa"],
            "Trasporti": ["Trasporto pubblico", "Carburante", "Parking and Tolls"],
            "Future": ["Work_New", "Education_New"]
        },
        "Volute_NonEssenziali": {
            "Selfcare(Clothes & Sport)": ["Abbigliamento & Scarpe", "Gifts", "Personal Care", "Sport & Fitness"],
            "Fun & Hobbies": ["Electronics", "Fun", "Hobby", "Adjust balance", "Unexpected"],
            "Travel & Events": ["Eventi", "Summer Holidays", "Weekends"]
        },
        "Affitto/Mutuo": {
                     "Affitto/Mutuo": ["Affitto/Mutuo",  "Beni immobili"]
        },
        "Nulle": {
            "Nulle": ["Education", "Correzioni", "Salary OUT", "Salary IN", "Trasferimento",
                       "Entrate da affitto", "Prelievo", "Work", "Placeholder", "Check Balance"]
        }
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

    @staticmethod
    def get_expenses_groups():
        CategoryStructure.check_expense_group()
        print("Verificare 'Beni Immobiliì' nel gruppo Entrate")
        print("Migliora il check expenses per evitare doppioni")
        print("Aggiungere due ulteriori gruppi: IN, Income_risparrmi, Out, Expense_risparmi")

        return CategoryStructure.expense_groups

    @staticmethod
    def get_expense_to_del():
        return CategoryStructure.expense_groups["Nulle"]["Nulle"]

    @staticmethod
    def check_expense_group():
        all_categories_of_expense_groups = []
        for expense_groups_name in CategoryStructure.expense_groups.keys():
            for categories_list in CategoryStructure.expense_groups[expense_groups_name].keys():
                all_categories_of_expense_groups.extend(
                    CategoryStructure.expense_groups[expense_groups_name][categories_list])

        all_basic_categories = CategoryStructure.get_basic_categories()

        category_difference = list(set(all_basic_categories) ^ set(all_categories_of_expense_groups))
        if len(category_difference) > 0:
            print("CategoryStructure.check_expense_group(): error", category_difference)
            raise TypeError