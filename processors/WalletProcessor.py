from processors.CategoryStructurer import CategoryStructurer
from processors.CategoryImporter import CategoryImporter
from processors.DataImporter import DataImporter
from processors.ExcelWriter import ExcelWriter
from processors.GroupCreator import GroupCreator


class WalletProcessor:

    def __init__(self, input_filename, time_period, output_filename=None, template_sheet_name=None):
        self.input_filename = input_filename
        if isinstance(time_period, str):
            self.time_period = time_period
        else:
            print("time_period is not a string")
            exit()
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
                year=self.time_period,
                # start_date="2023-12-25",
                # end_date="2023-12-31"
            )
            data = data_import.get_imported_data()
        except Exception as e:
            print("DataImport(): ", e)
            exit()

        try:
            category_importer = CategoryImporter()
            wallet_category_results = category_importer.process(data)
        except Exception as e:
            print("CategoryImporter(): ", e)
            exit()

        try:
            category_structurer = CategoryStructurer()
            main_category_results = category_structurer.process(wallet_category_results)
        except Exception as e:
            print("CategoryStructurer(): ", e)
            exit()

        try:
            group_creator = GroupCreator()
            group_results = group_creator.process(wallet_category_results)
            group_creator.check_amounts(group_results)

        except Exception as e:
            print("GroupCreator(): ", e)
            exit()

        # try:
        excel_writer = ExcelWriter(filename_in="Piano_Spesa_Template_v01.xlsx",
                                   template_sheetname="Template",
                                   output_sheet_name=self.time_period)

        excel_writer.write_main_category_results(main_category_results)
        excel_writer.write_group_results(group_results)
        print("===> Operazione Completata <===")
