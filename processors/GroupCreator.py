from data.CategoryResults import CategoryResults
from data.CategoryStructure import CategoryStructure


class GroupCreator:
    def __init__(self):
        self.expense_groups = CategoryStructure.get_expenses_groups()

    def process(self, data):
        if not isinstance(data, CategoryResults):
            raise TypeError("GroupCreator.process(): Wrong input type for data")

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
            main_category_in = 0
            main_category_out = 0
            main_category_savings = 0
            for sub_group_name in self.expense_groups[group_name].keys():
                sub_group_name_in = 0
                sub_group_name_out = 0
                sub_group_name_savings = 0
                for category_name in self.expense_groups[group_name][sub_group_name]:
                    sub_group_name_in += data.df.loc[category_name]["in"]
                    sub_group_name_out += data.df.loc[category_name]["out"]
                    sub_group_name_savings += data.df.loc[category_name]["savings"]
                    group_results.append(category_name, data.df.loc[category_name]["in"],
                                         data.df.loc[category_name]["out"], data.df.loc[category_name]["savings"])
                group_results.append(sub_group_name, sub_group_name_in, sub_group_name_out, sub_group_name_savings)
                main_category_in += sub_group_name_in
                main_category_out += sub_group_name_out
                main_category_savings += sub_group_name_savings
            group_results.append(group_name, main_category_in, main_category_out, main_category_savings)

        return group_results

    def check_amounts(self,group_results):
        if not isinstance(group_results, CategoryResults):
            raise TypeError("GroupCreator.check_amounts(): Wrong input type for data")

        for group_name in self.expense_groups.keys():
            if (group_results.df.loc[group_name]["in"] != 0) & (group_results.df.loc[group_name]["out"] != 0):
                print(group_name, "--> in:", group_results.df.loc[group_name]["in"], "out:",
                      group_results.df.loc[group_name]["out"])
                raise TypeError("GroupCreator.process(): in/out/saving distribution not valid")

