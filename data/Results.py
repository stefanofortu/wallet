import pandas as pd


class Results:
    def __init__(self):
        self.df = pd.DataFrame(columns=['category', 'in', 'savings_in', 'out', 'savings_out', 'no_tags'])

    def __str__(self):
        return self.df.to_string()

    def append(self, category, amount_in, amount_savings_in, amount_out, amount_savings_out, amount_no_tags):
        self.df.loc[category] = [category, amount_in, amount_savings_in, amount_out, amount_savings_out, amount_no_tags]
