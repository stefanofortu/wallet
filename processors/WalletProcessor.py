from processors.CategoryStructurer import CategoryStructurer
from processors.CategoryImporter import CategoryImporter
from processors.DataImporter import DataImporter
from processors.ExcelWriter import ExcelWriter
from processors.GroupCreator import GroupCreator
import logging

logger = logging.getLogger("Stefano")


class WalletProcessor:

    def __init__(self, input_filename, time_period, start_date, end_date, output_filename=None,
                 template_sheet_name=None):
        self.input_filename = input_filename
        self.start_date = None
        self.end_date = None
        self.output_sheet_name = self.set_start_end_date(time_period, start_date, end_date)

        if output_filename is None or output_filename == "" or \
                template_sheet_name is None or template_sheet_name == "":
            self.output_filename = "Piano_Spesa_Template_v01.xlsx"
            self.template_sheet_name = "Template"
        else:
            self.output_filename = output_filename
            self.template_sheet_name = template_sheet_name

    def execute(self):
        try:
            data_import = DataImporter(
                filename=self.input_filename,
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
        #try:
        group_creator = GroupCreator()
        group_results = group_creator.process(wallet_category_results)
        group_creator.check_amounts(group_results)

        #except Exception as e:
        #    logger.error("GroupCreator(): " + str(e))
        #    return

        # try:

        excel_writer = ExcelWriter(filename_in="Piano_Spesa_Template_v01.xlsx",
                                   template_sheetname="Template",
                                   output_sheet_name=self.output_sheet_name)

        excel_writer.write_main_category_results(main_category_results)
        excel_writer.write_group_results(group_results)
        logger.info("===> Operazione Completata <===")

    def set_start_end_date(self, year, start_date, end_date):
        if year is not None:
            if not isinstance(year, str):
                logger.error("time_period is not a string %s", year)
                raise TypeError
            else:
                self.start_date = year + "-01-01"
                self.end_date = year + "-12-31"
                return year
        else:
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
                    return start_date[0:4] + "_from_" + start_date[5:7] + "_to_" + end_date[5:7]