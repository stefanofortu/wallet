import pandas as pd


class CategoryResults:
    def __init__(self):
        self.df = pd.DataFrame(columns=['category', 'in', 'savings_in', 'out', 'savings_out'])

    def __str__(self):
        return self.df.to_string()

    def append(self, category, amount_in, amount_savings_in, amount_out, amount_savings_out):
        self.df.loc[category] = [category, amount_in, amount_savings_in, amount_out, amount_savings_out]
