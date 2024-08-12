from data.CategoryResults import CategoryResults
from data.CategoryStructure import CategoryStructure


class CategoryStructurer:
    def __init__(self):
        self.main_category = CategoryStructure.categories

    def process(self, data):
        if not isinstance(data, CategoryResults):
            raise TypeError("CategoryHierarchy.process(): Wrong input type for data")

        main_category_results = CategoryResults()
        for main_category in self.main_category.keys():
            main_cat_in = 0
            main_cat_out = 0
            main_cat_savings = 0
            for category in self.main_category[main_category]:
                main_cat_in += data.df.loc[category]["in"]
                main_cat_out += data.df.loc[category]["out"]
                main_cat_savings += data.df.loc[category]["savings_out"]

                main_category_results.append(category,
                                             amount_in=data.df.loc[category]["in"],
                                             amount_savings_in=0,
                                             amount_out=data.df.loc[category]["out"],
                                             amount_savings_out=data.df.loc[category]["savings_out"])
            main_category_results.append(main_category,
                                         amount_in=main_cat_in, amount_savings_in=0,
                                         amount_out=main_cat_out, amount_savings_out=main_cat_savings)
        return main_category_results
