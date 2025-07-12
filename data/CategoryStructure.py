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

    expense_groups = {
        "Redditi": {
            "Income": ["Salary", "Interessi & Dividendi", "Regali"]
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
        "Spese_Fisse": {
            "Spese_Immobiliari": ["Affitto/Mutuo", "Beni immobili"],
            "Rate_Auto": []
        },
        "Entrate_Casa": {
            "Entrate_Immobiliari": ["Quote"]
        },
        "Nulle": {
            "Spese_a_zero": ["Education", "Correzioni", "Salary OUT", "Salary IN", "TRANSFER",
                             "Entrate da affitto", "Prelievo", "Work", "Placeholder", "Check Balance"],
            "Crediti": ["Credito", "Restituzione credito"],
            "Prestiti": ["Prestito", "Refunds"],
            "Contabile": ["Contabile"]
        }
        # "Income_risparmi": {
        #     "Income": ["Salary", "Interessi & Dividendi", "Refunds", "Regali"]
        # },
        # "Expense_risparmi": {
        #     "Bollette_Manutenzione": ["Energia & Utenze", "Furniture, Maintenance", "Family"],
        #     "Macchina": ["Assicurazione veicoli", "Manutenzione veicoli"],
        #     "Salute_Beneficienza": ["Salute", "Beneficienza"],
        #     "Spesa_Caffe_Lunch": ["Bar & Locali", "Lunch", "Spesa"],
        #     "Trasporti": ["Trasporto pubblico", "Carburante", "Parking and Tolls"],
        #     "Future": ["Work_New", "Education_New"],
        #     "Selfcare(Clothes & Sport)": ["Abbigliamento & Scarpe", "Gifts", "Personal Care", "Sport & Fitness"],
        #     "Fun & Hobbies": ["Electronics", "Fun", "Hobby", "Adjust balance", "Unexpected"],
        #     "Travel & Events": ["Eventi", "Summer Holidays", "Weekends"],
        #     "Spese_Immobiliari": ["Affitto/Mutuo", "Beni immobili"],
        #     "Rate_Auto": []
        # }
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
        return CategoryStructure.expense_groups

    @staticmethod
    def get_income_categories():
        return list(CategoryStructure.expense_groups["Redditi"]["Income"])  # \
        # + \
        # list(CategoryStructure.expense_groups["Prestiti_Debiti"]["Crediti"])

    @staticmethod
    def get_expense_categories():
        return list([x for x in CategoryStructure.get_basic_categories()
                     if x not in CategoryStructure.get_income_categories()])

    @staticmethod
    def get_expense_to_del():
        return list(CategoryStructure.expense_groups["Nulle"]["Spese_a_zero"])

    @staticmethod
    def check_expense_group():
        # Get a list of all the categories
        all_basic_categories = CategoryStructure.get_basic_categories()

        # Get a list of all the categories from the expenses group
        all_categories_of_expense_groups = []
        for expense_groups_name in CategoryStructure.expense_groups.keys():
            for categories_list in CategoryStructure.expense_groups[expense_groups_name].keys():
                all_categories_of_expense_groups.extend(
                    CategoryStructure.expense_groups[expense_groups_name][categories_list])

        ##### Check for duplicated items ############
        duplicated_items = []
        for cat in all_basic_categories:
            if all_basic_categories.count(cat) > 1:
                duplicated_items.append(cat)
        if len(duplicated_items) > 0:
            logger.warning("Found duplicated items in \'all_basic_categories\'", set(duplicated_items))

        duplicated_items = []
        for cat in all_categories_of_expense_groups:
            if all_categories_of_expense_groups.count(cat) > 1:
                duplicated_items.append(cat)
        if len(duplicated_items) > 0:
            logger.warning("Found duplicated items in all_categories_of_expense_groups", set(duplicated_items))

        # if len(set(all_basic_categories)) != len(all_basic_categories):
        #  print("duplicates found in the list")

        ##### Check for duplicated items ############
        if len(set(all_categories_of_expense_groups)) != len(all_categories_of_expense_groups):
            logger.error("duplicates found in the list")

        ##### Check for duplicated items ############

        category_difference = list(set(all_basic_categories) ^ set(all_categories_of_expense_groups))
        if len(category_difference) > 0:
            logger.error("CategoryStructure.check_expense_group(): len(category_difference) > 0")
            print(category_difference)
            raise TypeError
