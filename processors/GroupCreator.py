from data.Results import Results
from data.CategoryStructure import CategoryStructure
from data.ExpenseGroups import ExpenseGroups
import logging

logger = logging.getLogger("Stefano")


class GroupCreator:
    def __init__(self):
        self.expense_groups = ExpenseGroups.get_expenses_groups()


    def process(self, data):
        if not isinstance(data, Results):
            raise TypeError("GroupCreator.process(): Wrong input type for data")

        all_categories_of_expense_groups = []
        for expense_groups_name in self.expense_groups.keys():
            for categories_list in self.expense_groups[expense_groups_name].keys():
                all_categories_of_expense_groups.extend(self.expense_groups[expense_groups_name][categories_list])

        all_basic_categories = CategoryStructure.get_basic_categories()

        category_difference = list(set(all_basic_categories) ^ set(all_categories_of_expense_groups))
        if len(category_difference) > 0:
            logger.critical("differenza in categoria", category_difference)
            exit()

        group_results = Results()
        for group_name in self.expense_groups.keys():
            main_group_in = 0
            main_group_savings_in = 0
            main_group_out = 0
            main_group_savings_out = 0
            for sub_group_name in self.expense_groups[group_name].keys():
                sub_group_name_in = 0
                sub_group_name_savings_in = 0
                sub_group_name_out = 0
                sub_group_name_savings_out = 0
                for category_name in self.expense_groups[group_name][sub_group_name]:
                    sub_group_name_in += data.df.loc[category_name]["in"]
                    sub_group_name_savings_in += data.df.loc[category_name]["savings_in"]
                    sub_group_name_out += data.df.loc[category_name]["out"]
                    sub_group_name_savings_out += data.df.loc[category_name]["savings_out"]
                    group_results.append(category_name,
                                         amount_in=data.df.loc[category_name]["in"],
                                         amount_savings_in=data.df.loc[category_name]["savings_in"],
                                         amount_out=data.df.loc[category_name]["out"],
                                         amount_savings_out=data.df.loc[category_name]["savings_out"],
                                         amount_no_tags=0)
                group_results.append(sub_group_name,
                                     amount_in=sub_group_name_in,
                                     amount_savings_in=sub_group_name_savings_in,
                                     amount_out=sub_group_name_out,
                                     amount_savings_out=sub_group_name_savings_out,
                                     amount_no_tags=0)
                main_group_in += sub_group_name_in
                main_group_savings_in += sub_group_name_savings_in
                main_group_out += sub_group_name_out
                main_group_savings_out += sub_group_name_savings_out
            group_results.append(group_name,
                                 amount_in=main_group_in,
                                 amount_savings_in=main_group_savings_in,
                                 amount_out=main_group_out,
                                 amount_savings_out=main_group_savings_out,
                                 amount_no_tags=0)

        logger.info("Merge of categories into main categories: DONE")

        self.check_amounts_both_positive_and_negative(group_results)
        logger.info("Check sign of the main categories: DONE")

        return group_results

    def check_amounts_both_positive_and_negative(self, group_results):
        for group_name in self.expense_groups.keys():
            if (group_results.df.loc[group_name]["in"] != 0) & (group_results.df.loc[group_name]["out"] != 0):
                logger.warning(group_name + str("--> in:") + str(group_results.df.loc[group_name]["in"])
                               + str(" out:") + str(group_results.df.loc[group_name]["out"]))
                raise TypeError("GroupCreator.process(): in/out/saving distribution not valid")
