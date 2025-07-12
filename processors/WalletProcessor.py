from processors.CategoryStructurer import CategoryStructurer
from processors.CategoryImporter import CategoryImporter
from processors.DataImporter import DataImporter
from processors.ExcelWriter import ExcelWriter
from processors.GroupCreator import GroupCreator
import logging

logger = logging.getLogger("Stefano")


class WalletProcessor:

    def __init__(self, input_filename, main_wallet_selection, start_date, end_date, output_filename=None,
                 template_sheet_name=None):
        self.input_filename = input_filename
        self.start_date = None
        self.end_date = None
        self.set_start_end_date(start_date, end_date)
        self.main_wallet_selection = main_wallet_selection

        if output_filename is None or output_filename == "" or \
                template_sheet_name is None or template_sheet_name == "":
            self.output_filename = "Piano_Spesa_Template_v01.xlsx"
            self.template_sheet_name = "Template"
        else:
            self.output_filename = output_filename
            self.template_sheet_name = template_sheet_name
        self.output_sheet_name = "from_" + self.start_date + "_to_" + self.end_date

    def execute(self):
        try:
            data_import = DataImporter(
                filename=self.input_filename,
                main_wallet_selection=self.main_wallet_selection,
                start_date=self.start_date,
                end_date=self.end_date
            )
            data = data_import.get_imported_data()
        except Exception as e:
            logger.error("DataImport(): " + str(e))
            return

        try:
            category_importer = CategoryImporter()
            wallet_category_results = category_importer.process(data)
        except Exception as e:
            logger.error("CategoryImporter(): " + str(e))
            return
        try:
            category_structurer = CategoryStructurer()
            main_category_results = category_structurer.process(wallet_category_results)
        except Exception as e:
            logger.error("CategoryStructurer(): " + str(e))
            return
        try:
            group_creator = GroupCreator()
            group_results = group_creator.process(wallet_category_results)
            group_creator.check_amounts(group_results)
        except Exception as e:
            logger.error("GroupCreator(): " + str(e))
            return

        # try:

        excel_writer = ExcelWriter(filename_in="Piano_Spesa_Template_v01.xlsx",
                                   template_sheetname="Template",
                                   sheetname_title=self.output_sheet_name)

        excel_writer.write_main_category_results(main_category_results)
        excel_writer.write_group_results(group_results)
        logger.info("===> Operazione Completata <===")

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