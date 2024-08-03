from processors.CategoryStructurer import CategoryStructurer
from processors.CategoryImporter import CategoryImporter
from processors.DataImporter import DataImporter
from processors.ExcelWriter import ExcelWriter
from processors.GroupCreator import GroupCreator
from datetime import datetime


def wallet_process_app():

    time_period = "2023"
    try:
        data_import = DataImporter(
            filename="C:\\Users\\Stefano\\Documents\\MEGA\\MegaSync_Pixel\\report_2024-08-03_162051.xls",
            year=time_period,
            #start_date="2023-12-25",
            #end_date="2023-12-31"
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
    except Exception as e:
        print("CategoryImport(): ", e)
        exit()

    filename = str(datetime.now().strftime("%Y%m%d_%Hh%Mm%Ss")) + ".xlsx"
    excel_writer = ExcelWriter(filename, time_period)
    excel_writer.process(main_category_results, group_results)




if __name__ == '__main__':
    wallet_process_app()
