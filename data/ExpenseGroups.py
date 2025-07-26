from data.CategoryStructure import CategoryStructure
import logging

logger = logging.getLogger("Stefano")


class ExpenseGroups:
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
            "Entrate_Immobiliari": ["Quote", "Entrate da affitto"]
        },
        "ALTRO": {
            "Spese_a_zero": ["Education", "Correzioni", "Prelievo", "Work", "Placeholder", "Check Balance"],
            "Crediti": ["Credito", "Restituzione credito"],
            "Prestiti": ["Prestito", "Refunds"],
            "Trasferimenti": ["TRANSFER"],
            "Contabile": ["Contabile"],
            "Salary_IN_OUT": ["Salary OUT", "Salary IN"]
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
    def get_expenses_groups():
        ExpenseGroups.check_expense_group()
        return ExpenseGroups.expense_groups

    @staticmethod
    def get_income_categories():
        return list(ExpenseGroups.expense_groups["Redditi"]["Income"]) + \
               list(ExpenseGroups.expense_groups["Entrate_Casa"]["Entrate_Immobiliari"])

    @staticmethod
    def get_categories_null_balance():
        return list(ExpenseGroups.expense_groups["ALTRO"]["Crediti"]) + \
               list(ExpenseGroups.expense_groups["ALTRO"]["Prestiti"]) + \
               list(ExpenseGroups.expense_groups["ALTRO"]["Trasferimenti"]) + \
               list(ExpenseGroups.expense_groups["ALTRO"]["Contabile"]) + \
               list(ExpenseGroups.expense_groups["ALTRO"]["Salary_IN_OUT"])

    @staticmethod
    def get_expense_categories():
        income_cat = ExpenseGroups.get_income_categories()
        null_balance_cat = ExpenseGroups.get_categories_null_balance()

        return list([x for x in CategoryStructure.get_basic_categories()
                     if x not in income_cat and x not in null_balance_cat] )
        # \
        # + \
        # list(CategoryStructure.expense_groups["Prestiti_Debiti"]["Crediti"])

    @staticmethod
    def get_expense_to_del():
        return list(ExpenseGroups.expense_groups["ALTRO"]["Spese_a_zero"])

    @staticmethod
    def check_expense_group():
        # Get a list of all the categories
        all_basic_categories = CategoryStructure.get_basic_categories()

        # Get a list of all the categories from the expenses group
        all_categories_of_expense_groups = []
        for expense_groups_name in ExpenseGroups.expense_groups.keys():
            for categories_list in ExpenseGroups.expense_groups[expense_groups_name].keys():
                all_categories_of_expense_groups.extend(
                    ExpenseGroups.expense_groups[expense_groups_name][categories_list])

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
            logger.error(f" category_difference: {category_difference}")
