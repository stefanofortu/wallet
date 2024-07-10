import pandas as pd
import xlsxwriter

from data.CategoryResults import CategoryResults
from data.CategoryStructure import CategoryStructure

from win32com.client import Dispatch


class ExcelWriter:
    def __init__(self, filename, sheetname):
        self.filename = filename
        self.sheetname = sheetname

        self.wb = xlsxwriter.Workbook(self.filename)
        self.ws = self.wb.add_worksheet(self.sheetname)
        self.ws.outline_settings(symbols_below=False)
        self.writer = pd.ExcelWriter(self.filename, engine='xlsxwriter')

    def __del__(self):
        self.ws.autofit()
        self.wb.close()

    def process(self, main_category_results, group_results):
        if not isinstance(main_category_results, CategoryResults):
            print("ExcelWriter.process(): Wrong input type for data main_category_results")
            raise TypeError
        if not isinstance(group_results, CategoryResults):
            print("ExcelWriter.process(): Wrong input type for data group_results")
            raise TypeError

        row_num = 0
        for main_cat in list(CategoryStructure.categories.keys()):
            self.ws.write(row_num, 0, main_cat)
            self.ws.write(row_num, 1, main_category_results.df.loc[main_cat]["amount"])
            self.ws.set_row(row_num, None, None, {'collapsed': True})
            row_num += 1
            for cat in list(CategoryStructure.categories[main_cat]):
                self.ws.write(row_num, 0, cat)
                self.ws.write(row_num, 1, main_category_results.df.loc[cat]["amount"])
                self.ws.set_row(row_num, None, None, {'level': 1, 'hidden': True})
                row_num += 1

        row_num += 3
        for main_group in list(CategoryStructure.expense_groups.keys()):
            self.ws.write(row_num, 0, main_group)
            self.ws.write(row_num, 1, group_results.df.loc[main_group]["amount"])
            self.ws.set_row(row_num, None, None, {'collapsed': True})
            row_num += 1
            for sub_group in CategoryStructure.expense_groups[main_group].keys():
                self.ws.write(row_num, 0, sub_group)
                self.ws.write(row_num, 1, group_results.df.loc[sub_group]["amount"])
                self.ws.set_row(row_num, None, None, {'level': 1, 'hidden': True})
                row_num += 1
                for cat in list(CategoryStructure.expense_groups[main_group][sub_group]):
                    self.ws.write(row_num, 0, cat)
                    self.ws.write(row_num, 1, group_results.df.loc[cat]["amount"])
                    self.ws.set_row(row_num, None, None, {'level': 2, 'hidden': True})
                    row_num += 1
