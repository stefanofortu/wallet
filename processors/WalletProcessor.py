from data.ExpenseGroups import ExpenseGroups
from processors.CategoryStructurer import CategoryStructurer
from processors.CategoryLabelChecker import CategoryLabelChecker
from processors.CategoryClassification import CategoryClassification
from processors.DataImporter import DataImporter
from processors.ExcelWriter import ExcelWriter
from processors.GroupCreator import GroupCreator
import logging

logger = logging.getLogger("Stefano")


class WalletProcessor:

    def __init__(self, input_filename, main_wallet_selection, start_date, end_date):
        self.input_filename = input_filename
        self.start_date = None
        self.end_date = None
        self.set_start_end_date(start_date, end_date)
        self.main_wallet_selection = main_wallet_selection

        ExpenseGroups.check_expense_group()

    def execute(self):
        logger.info("Processing Started")
        data_import = DataImporter(
            filename=self.input_filename,
            main_wallet_selection=self.main_wallet_selection,
            start_date=self.start_date,
            end_date=self.end_date
        )
        data = data_import.get_imported_data()

        category_and_label_checker = CategoryLabelChecker(main_wallet_selection = self.main_wallet_selection)
        results_ok = category_and_label_checker.process(data)
        if not results_ok:
            logger.error("CategoryLabelChecker outcome not OK")

        data.all_data.to_excel("all_data.xlsx")

        category_classifier = CategoryClassification()
        wallet_category_results = category_classifier.process(data)
        wallet_category_results.df.to_excel("wallet_category_results.xlsx")

        category_structurer = CategoryStructurer()
        main_category_results = category_structurer.process(wallet_category_results)
        main_category_results.df.to_excel("main_category_results.xlsx")

        group_creator = GroupCreator()
        group_results = group_creator.process(wallet_category_results)

        excel_writer = ExcelWriter(filename_in="Piano_Spesa_Template_v02.xlsx",
                                   template_sheetname="Template",
                                   sheetname_title=("from_" + self.start_date + "_to_" + self.end_date))

        excel_writer.write_main_category_results(main_category_results)
        excel_writer.write_group_results(group_results)
        logger.info("Processing Completed.")

    def set_start_end_date(self, start_date, end_date):
        if start_date is None and end_date is None:
            logger.error("Error in year | start_data | end_date input")
            raise TypeError
        else:
            if not isinstance(start_date, str):
                logger.error("start_date is not a string %s", start_date)
                raise TypeError
            else:
                self.start_date = start_date
            if not isinstance(end_date, str):
                logger.error("end_date is not a string %s", end_date)
                exit()
            else:
                self.end_date = end_date