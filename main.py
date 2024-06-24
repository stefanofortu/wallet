import xlsxwriter
from processors.CategoryStructurer import CategoryStructurer
from processors.CategoryImporter import CategoryImporter
from processors.DataImporter import DataImporter
from processors.ExcelWriter import ExcelWriter
from processors.GroupCreator import GroupCreator


def wallet_process_app():
    try:
        data_import = DataImporter(
            filename="C:\\Users\\Stefano\\Documents\\MEGA\\MegaSync_Pixel\\report_2024-06-23.xls",
            year="2023"
        )
        data_2024 = data_import.get_imported_data()
    except Exception as e:
        print("DataImport(): ".format(e))
        exit()

    try:
        category_importer = CategoryImporter()
        wallet_category = category_importer.process(data_2024)
    except Exception as e:
        print("CategoryImport() :".format(e))
        exit()

    try:
        category_structurer = CategoryStructurer()
        main_category = category_structurer.process(wallet_category)
    except Exception as e:
        print("CategoryImport() :".format(e))
        exit()

    #try:
    group_creator = GroupCreator()
    _ = group_creator.process(wallet_category)
    #except Exception as e:
    #    print("CategoryImport() :".format(e))
    #    exit()


    excel_writer = ExcelWriter("pandas_text.xlsx", "2024")
    excel_writer.process(main_category, wallet_category)


if __name__ == '__main__':
    wallet_process_app()
