from data.Results import Results
from data.CategoryStructure import CategoryStructure
from data.WalletData import WalletData
import logging

logger = logging.getLogger("Stefano")


class CategoryClassification:
    def __init__(self):
        self.all_category = CategoryStructure.get_basic_categories()
        logger.warning("Aggiungere due ulteriori gruppi: IN, Income_risparmi, Out, Expense_risparmi. Da gestire "
                       "correttamente")

    def process(self, data):
        if not isinstance(data, WalletData):
            logger.error("Category_Label_Checker(): Wrong input type for data")

        # data.df_main.amount = data.df_main.amount.round(2)
        category_results = Results()
        for category in self.all_category:
            filtered_data_in = data.all_data[(data.all_data["category"] == category) &
                                            (data.all_data["labels"] == "in")]
            filtered_data_in.reset_index(inplace=True)
            amount_in = round(filtered_data_in['amount'].sum(), 2)

            filtered_data_out = data.all_data[(data.all_data["category"] == category) &
                                             (data.all_data["labels"] == "out")]
            filtered_data_out.reset_index(inplace=True)
            amount_out = round(filtered_data_out['amount'].sum(), 2)

            filtered_data_savings = data.all_data[(data.all_data["category"] == category) &
                                                 (data.all_data["labels"] == "risparmi")]
            filtered_data_savings.reset_index(inplace=True)
            amount_savings = round(filtered_data_savings['amount'].sum(), 2)

            if amount_savings >= 0:
                amount_savings_in = amount_savings
                amount_savings_out = 0
            else:
                amount_savings_in = 0
                amount_savings_out = amount_savings

            filtered_data_savings = data.all_data[(data.all_data["category"] == category) &
                                                 (data.all_data["labels"] == "no_tags")]
            filtered_data_savings.reset_index(inplace=True)
            amount_no_tags = round(filtered_data_savings['amount'].sum(), 2)

            category_results.append(category,
                                    amount_in=amount_in, amount_savings_in=amount_savings_in,
                                    amount_out=amount_out, amount_savings_out=amount_savings_out,
                                    amount_no_tags=amount_no_tags)
        logger.info("Split of all categories by tags: DONE")
        logger.info("Calculation of values of basic categories: DONE")

        return category_results
