from data.Results import Results
from data.CategoryStructure import CategoryStructure
import logging

logger = logging.getLogger("Stefano")


class CategoryStructurer:
    def __init__(self):
        self.main_category = CategoryStructure.categories

    def process(self, data):
        if not isinstance(data, Results):
            raise TypeError("CategoryHierarchy.process(): Wrong input type for data")

        main_category_results = Results()
        for main_category in self.main_category.keys():
            main_cat_in = 0
            main_cat_savings_in = 0
            main_cat_out = 0
            main_cat_savings_out = 0
            main_cat_no_tags = 0
            for category in self.main_category[main_category]:
                main_cat_in += data.df.loc[category]["in"]
                main_cat_savings_in += data.df.loc[category]["savings_in"]
                main_cat_out += data.df.loc[category]["out"]
                main_cat_savings_out += data.df.loc[category]["savings_out"]
                main_cat_no_tags += data.df.loc[category]["no_tags"]
                main_category_results.append(category,
                                             amount_in=data.df.loc[category]["in"],
                                             amount_savings_in=data.df.loc[category]["savings_in"],
                                             amount_out=data.df.loc[category]["out"],
                                             amount_savings_out=data.df.loc[category]["savings_out"],
                                             amount_no_tags=data.df.loc[category]["no_tags"])
            main_category_results.append(main_category,
                                         amount_in=main_cat_in,
                                         amount_savings_in=main_cat_savings_in,
                                         amount_out=main_cat_out,
                                         amount_savings_out=main_cat_savings_out,
                                         amount_no_tags=main_cat_no_tags)

        logger.info("Calculation of values of main categories: DONE")
        return main_category_results
