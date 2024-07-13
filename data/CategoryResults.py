import pandas as pd


class CategoryResults:
    def __init__(self):
        self.df = pd.DataFrame(columns=['category', 'in', 'out', 'savings'])

    def __str__(self):
        return self.df.to_string()

    def append(self, category, amount_in, amount_out, amount_savings):
        self.df.loc[category] = [category, amount_in, amount_out, amount_savings]
