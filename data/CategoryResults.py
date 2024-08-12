import pandas as pd


class CategoryResults:
    def __init__(self):
        self.df = pd.DataFrame(columns=['category', 'in', 'savings_in', 'out', 'savings_out'])

    def __str__(self):
        return self.df.to_string()

    def append(self, category, amount_in, amount_savings_in, amount_out, amount_savings_out):
        self.df.loc[category] = [category, amount_in, amount_savings_in, amount_out, amount_savings_out]


class RegularExpenseResults:
    def __init__(self, category_results=None):
        if category_results is None:
            self.df = pd.DataFrame(columns=['category', 'in', 'out'])
        else:
            if not isinstance(category_results, CategoryResults):
                raise TypeError("RegularExpenseResults.__init__(): Wrong input type for data")
            self.df = category_results.df[['category', 'in', 'out']].copy()

    def __str__(self):
        return self.df.to_string()

    def append(self, category, amount_in, amount_out):
        self.df.loc[category] = [category, amount_in, amount_out]
        print("This method should never be used")


class SavingResults:
    def __init__(self, category_results=None):
        if category_results is None:
            self.df = pd.DataFrame(columns=['category', 'savings_in', 'savings_out'])
        else:
            if not isinstance(category_results, CategoryResults):
                raise TypeError("RegularExpenseResults.__init__(): Wrong input type for data")
            self.df = category_results.df[['category', 'in', 'out']].copy()

    def __str__(self):
        return self.df.to_string()

    def append(self, category, amount_savings_in, amount_savings_out):
        self.df.loc[category] = [category, amount_savings_in, amount_savings_out]
        print("This method should never be used")
