from data.Results import Results
from data.CategoryStructure import CategoryStructure
from data.ExpenseGroups import ExpenseGroups
from data.WalletData import WalletData
import logging
from utils.LoggingStream import df_logger

logger = logging.getLogger("Stefano")

class GroupCreator:
    def __init__(self):
        self.expense_groups = ExpenseGroups.get_expenses_groups()

    def process(self, wallet_category_results, wallet_data):
        if not isinstance(wallet_category_results, Results):
            raise TypeError("GroupCreator.process(): Wrong input type for data")
        if not isinstance(wallet_data, WalletData):
            raise TypeError("GroupCreator.process(): Wrong input type for data")
        wlc = wallet_category_results
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
            main_group_no_tags = 0
            for sub_group_name in self.expense_groups[group_name].keys():
                sub_group_name_in = 0
                sub_group_name_savings_in = 0
                sub_group_name_out = 0
                sub_group_name_savings_out = 0
                sub_group_name_no_tags = 0
                for category_name in self.expense_groups[group_name][sub_group_name]:
                    sub_group_name_in += wlc.df.loc[category_name]["in"]
                    sub_group_name_savings_in += wlc.df.loc[category_name]["savings_in"]
                    sub_group_name_out += wlc.df.loc[category_name]["out"]
                    sub_group_name_savings_out += wlc.df.loc[category_name]["savings_out"]
                    sub_group_name_no_tags += wlc.df.loc[category_name]["no_tags"]
                    group_results.append(category_name,
                                         amount_in=wlc.df.loc[category_name]["in"],
                                         amount_savings_in=wlc.df.loc[category_name]["savings_in"],
                                         amount_out=wlc.df.loc[category_name]["out"],
                                         amount_savings_out=wlc.df.loc[category_name]["savings_out"],
                                         amount_no_tags=wlc.df.loc[category_name]["no_tags"])
                group_results.append(sub_group_name,
                                     amount_in=sub_group_name_in,
                                     amount_savings_in=sub_group_name_savings_in,
                                     amount_out=sub_group_name_out,
                                     amount_savings_out=sub_group_name_savings_out,
                                     amount_no_tags=sub_group_name_no_tags)
                main_group_in += sub_group_name_in
                main_group_savings_in += sub_group_name_savings_in
                main_group_out += sub_group_name_out
                main_group_savings_out += sub_group_name_savings_out
                main_group_no_tags += sub_group_name_no_tags
            group_results.append(group_name,
                                 amount_in=main_group_in,
                                 amount_savings_in=main_group_savings_in,
                                 amount_out=main_group_out,
                                 amount_savings_out=main_group_savings_out,
                                 amount_no_tags=main_group_no_tags)

        logger.info("Merge of categories into main categories: DONE")

        self.check_amounts_both_positive_and_negative(group_results=group_results)
        logger.info("Check sign of the main categories: DONE")

        #################### CREDITI ####################
        sum_result = self.check_group_has_sum_zero(group_results=group_results, group_name="ALTRO",
                                                   subgroup_name="Crediti")
        logger.info(f"Check total sum of the category Credit...DONE")

        self.find_data_not_zero_sum(wallet_data=wallet_data, group_name="ALTRO",
                                    subgroup_name="Crediti", computed_sum=sum_result)

        #################### PRESTITI ####################
        sum_result = self.check_group_has_sum_zero(group_results=group_results, group_name="ALTRO",
                                                   subgroup_name="Prestiti")
        logger.info(f"Check total sum of the category Prestiti...DONE")

        self.find_data_not_zero_sum(wallet_data=wallet_data, group_name="ALTRO",
                                    subgroup_name="Prestiti", computed_sum=sum_result)

        #################### TRASFERIMENTI ####################
        sum_result = self.check_group_has_sum_zero(group_results=group_results, group_name="ALTRO",
                                                   subgroup_name="Trasferimenti")
        logger.info(f"Check total sum of the category Trasferimenti...DONE")
        logger.info(f"Check of all the trasnfers by ID makes no sense")

        #################### CONTABILE ####################
        sum_result = self.check_group_has_sum_zero(group_results=group_results, group_name="ALTRO",
                                                   subgroup_name="Contabile")
        logger.info(f"Check total sum of the category Contabile...DONE")

        self.find_data_not_zero_sum(wallet_data=wallet_data, group_name="ALTRO",
                                    subgroup_name="Contabile", computed_sum=sum_result)

        #################### SALARY IN/OUT ####################
        sum_result = self.check_group_has_sum_zero(group_results=group_results, group_name="ALTRO",
                                                   subgroup_name="Salary_IN_OUT")
        logger.info(f"Check total sum of the category Salary_IN_OUT...DONE")
        self.find_data_not_zero_sum(wallet_data=wallet_data, group_name="ALTRO",
                                    subgroup_name="Salary_IN_OUT", computed_sum=sum_result)

        return group_results

    def check_amounts_both_positive_and_negative(self, group_results):
        for group_name in self.expense_groups.keys():
            if (group_results.df.loc[group_name]["in"] != 0) & (group_results.df.loc[group_name]["out"] != 0):
                logger.warning(group_name + str("--> in:") + str(group_results.df.loc[group_name]["in"])
                               + str(" out:") + str(group_results.df.loc[group_name]["out"]))
                logger.warning("GroupCreator.process(): check_amounts_both_positive_and_negative")

    @staticmethod
    def check_group_has_sum_zero(group_results, group_name, subgroup_name):
        row_sum = group_results.df.loc[[subgroup_name],
                                       ['in', 'savings_in', 'out', 'savings_out', 'no_tags']].sum(axis=1)
        if row_sum.shape[0] == 1:
            row_sum = round(row_sum.iloc[0], 2)

        if row_sum == 0:
            logger.info(f"GROUP RESULT: {subgroup_name} is zero")
        else:
            logger.warning(f"GROUP RESULT: {subgroup_name} is not zero: {row_sum}")
        return row_sum

    @staticmethod
    def find_data_not_zero_sum(wallet_data, group_name, subgroup_name, computed_sum):
        # logger.info(f"find_data_not_zero_sum: {group_name}, {subgroup_name}.......")
        logger.info(f'"################### {subgroup_name} START #######################"')
        category_list = (ExpenseGroups.get_expense_from_group(group=group_name, subgroup=subgroup_name))

        mask_filtered_df = wallet_data.all_data['category'].isin(category_list)
        filtered_df = wallet_data.all_data[mask_filtered_df].copy()
        filtered_df['transaction_ID'] = filtered_df['note'].str.extract(r'\[(.*?)\]')
        # print(filtered_df[['date', 'account', 'category', 'amount', 'transaction_ID']])

        df_transaction_id_nan = filtered_df[filtered_df['transaction_ID'].isna()]
        df_transaction_id_not_nan = filtered_df[filtered_df['transaction_ID'].notna()]

        # filtered_df_no_nan = filtered_df.dropna()
        # print(filtered_df_no_nan[['date', 'account', 'category', 'amount', 'transaction_ID']])

        # Conta quante volte ciascun trasferimento ha una specifica data
        # conteggio = df_transaction_id_not_nan['transaction_ID'].value_counts()

        list_id = df_transaction_id_not_nan['transaction_ID'].unique()
        for id in list_id:
            df_with_id = df_transaction_id_not_nan[df_transaction_id_not_nan['transaction_ID'] == id]
            sum_df_with_id = round(df_with_id['amount'].sum(), 2)
            if sum_df_with_id != 0:
                logger.warning(f"Transitions with ID {id} has sum {sum_df_with_id}")

        if not df_transaction_id_nan.empty:
            logger.warning(f"filtered_df contains transitions with no ID")
            df_logger.print_df_tabulated(df_transaction_id_nan)
        # Seleziona i valori che compaiono almeno due volte
        # value_with_at_least_one_match = conteggio[conteggio >= 2].index

        # df_with_at_least_one_match = filtered_df[filtered_df['transaction_ID'].isin(value_with_at_least_one_match)]
        # sum_with_at_least_one_match = round(df_with_at_least_one_match['amount'].sum(), 2)

        # if sum_with_at_least_one_match != 0.0:
        #    logger.warning(f"sum_with_at_least_one_match != 0.0 : {sum_with_at_least_one_match}")
        #    logger.info(f"df_with_at_least_one_match: ")
        #    wallet_data.print_df_tabulated(df_with_at_least_one_match)

        # df_with_no_match = filtered_df[~filtered_df['transaction_ID'].isin(value_with_at_least_one_match)]
        # sum_with_no_match = round(df_with_no_match['amount'].sum(), 2)

        # if sum_with_no_match != computed_sum or sum_with_no_match == 0.0:
        #    logger.warning(f"sum_with_no_match != computed_sum: {sum_with_no_match}, {computed_sum}")
        #    print()
        #    print(df_with_no_match[['category', 'amount', 'transaction_ID']])

        # if sum_with_no_match == computed_sum:
        #    logger.info(f"sum_with_no_match == computed_sum: {sum_with_no_match}")
        # logger.info(f"find_data_not_zero_sum: {group_name}, {subgroup_name}.......DONE")
        logger.info(f'"################### {subgroup_name} END #######################"')
