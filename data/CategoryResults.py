import pandas as pd


class CategoryResults:
    def __init__(self):
        self.df = pd.DataFrame(columns=['category', 'amount'])

    def __str__(self):
        return self.df.to_string()

    def append(self, category, amount):
        self.df.loc[category] = [category, amount]
