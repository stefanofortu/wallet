from datetime import datetime

import pandas as pd
import openpyxl

from data.CategoryResults import CategoryResults
from data.CategoryStructure import CategoryStructure

from win32com.client import Dispatch


class ExcelWriter:
    def __init__(self, filename_in, sheetname):
        self.filename_in = filename_in
        self.sheetname = sheetname
        self.filename_out = self.create_output_name()

        self.wb = openpyxl.load_workbook(self.filename_in)
        self.ws = self.wb.get_sheet_by_name(self.sheetname)
        #self.ws.outline_settings(symbols_below=False)
        #self.writer = pd.ExcelWriter(self.filename_in, engine='xlsxwriter')


    def create_output_name(self):
        filename_in_no_extension = self.filename_in.split(".")[0]
        extension = self.filename_in.split(".")[1]
        base_name = filename_in_no_extension.split("_v")[0]
        version = int(filename_in_no_extension.split("_v")[1])
        filename = str(datetime.now().strftime("%Y%m%d_%Hh%Mm%Ss"))
        filename_out = base_name + "_" + str(version).zfill(2) + "_" + filename + "." + extension
        return filename_out

    def __del__(self):
        #self.ws.autofit()
        #self.wb.close()
        pass

    def process(self, main_category_results, group_results):
        if not isinstance(main_category_results, CategoryResults):
            print("ExcelWriter.process(): Wrong input type for data main_category_results")
            raise TypeError
        if not isinstance(group_results, CategoryResults):
            print("ExcelWriter.process(): Wrong input type for data group_results")
            raise TypeError

        _category_column = 1
        _in_column = 2
        _out_column = 3
        _savings_column = 4

        row_num = 1
        self.ws.cell(row=row_num, column=_category_column).value  ="Categories"
        self.ws.cell(row_num, _in_column, "in")
        self.ws.cell(row_num, _out_column, "out")
        self.ws.cell(row_num, _savings_column, "savings")
        row_num += 1

        print(self.filename_out)
        self.wb.save(self.filename_out)
        self.wb.close()
        exit()
        return
        for main_cat in list(CategoryStructure.categories.keys()):
            self.ws.write(row_num, 0, main_cat)
            self.ws.write(row_num, 1, main_category_results.df.loc[main_cat]["in"])
            self.ws.write(row_num, 2, main_category_results.df.loc[main_cat]["out"])
            self.ws.write(row_num, 3, main_category_results.df.loc[main_cat]["savings"])
            self.ws.set_row(row_num, None, None, {'collapsed': True})
            row_num += 1
            for cat in list(CategoryStructure.categories[main_cat]):
                self.ws.write(row_num, 0, cat)
                self.ws.write(row_num, 1, main_category_results.df.loc[cat]["in"])
                self.ws.write(row_num, 2, main_category_results.df.loc[cat]["out"])
                self.ws.write(row_num, 3, main_category_results.df.loc[cat]["savings"])
                self.ws.set_row(row_num, None, None, {'level': 1, 'hidden': True})
                row_num += 1

        self.ws.write(row_num, 0, "-")
        self.ws.write(row_num, 1, "-")
        self.ws.write(row_num, 2, "-")
        self.ws.write(row_num, 3, "-")
        row_num += 1
        for main_group in list(CategoryStructure.expense_groups.keys()):
            self.ws.write(row_num, 0, main_group)
            self.ws.write(row_num, 1, group_results.df.loc[main_group]["in"])
            self.ws.write(row_num, 2, group_results.df.loc[main_group]["out"])
            self.ws.write(row_num, 3, group_results.df.loc[main_group]["savings"])
            self.ws.set_row(row_num, None, None, {'collapsed': True})
            row_num += 1
            for sub_group in CategoryStructure.expense_groups[main_group].keys():
                self.ws.write(row_num, 0, sub_group)
                self.ws.write(row_num, 1, group_results.df.loc[sub_group]["in"])
                self.ws.write(row_num, 2, group_results.df.loc[sub_group]["out"])
                self.ws.write(row_num, 3, group_results.df.loc[sub_group]["savings"])
                self.ws.set_row(row_num, None, None, {'level': 1, 'hidden': True})
                row_num += 1
                for cat in list(CategoryStructure.expense_groups[main_group][sub_group]):
                    self.ws.write(row_num, 0, cat)
                    self.ws.write(row_num, 1, group_results.df.loc[cat]["in"])
                    self.ws.write(row_num, 2, group_results.df.loc[cat]["out"])
                    self.ws.write(row_num, 3, group_results.df.loc[cat]["savings"])
                    self.ws.set_row(row_num, None, None, {'level': 2, 'hidden': True})
                    row_num += 1
