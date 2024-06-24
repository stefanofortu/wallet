from data.CategoryResults import CategoryResults
from data.CategoryStructure import CategoryStructure


class GroupCreator:
    def __init__(self):
        self.expense_groups = CategoryStructure.get_expenses_groups()

    def process(self, data):
        if not isinstance(data, CategoryResults):
            print("CategoryHierarchy.process(): Wrong input type for data")
            raise TypeError

        all_categories_of_expense_groups = []
        for expense_groups_name in self.expense_groups.keys():
            for categories_list in self.expense_groups[expense_groups_name].keys():
                all_categories_of_expense_groups.extend(self.expense_groups[expense_groups_name][categories_list])

        all_basic_categories = CategoryStructure.get_basic_categories()

        category_difference = list(set(all_basic_categories) ^ set(all_categories_of_expense_groups))
        if len(category_difference) > 0:
            print("differenza in categoria", category_difference)
            exit()


        group_results = CategoryResults()
        for group_name in self.expense_groups.keys():
            main_category_amount = 0
            for sub_group_name in self.expense_groups[group_name].keys():
                sub_group_name_amount = 0
                for category_name in self.expense_groups[group_name][sub_group_name]:
                    sub_group_name_amount += data.df.loc[category_name]["amount"]
                    group_results.append(category_name, data.df.loc[category_name]["amount"])
                group_results.append(sub_group_name, sub_group_name_amount)
                main_category_amount += sub_group_name_amount
            group_results.append(group_name, main_category_amount)