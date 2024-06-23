from data.CategoryResults import CategoryResults
from data.CategoryStructure import CategoryStructure


class CategoryStructurer:
    def __init__(self):
        self.main_category = CategoryStructure.categories

    def process(self, data):
        if not isinstance(data, CategoryResults):
            print("CategoryHierarchy.process(): Wrong input type for data")
            raise TypeError

        main_category_results = CategoryResults()
        for main_category in self.main_category.keys():
            main_category_amount = 0
            for category in self.main_category[main_category]:
                main_category_amount += data.df.loc[category]["amount"]
                main_category_results.append(main_category, main_category_amount)
        return main_category_results
