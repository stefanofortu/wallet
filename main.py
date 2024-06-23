import xlsxwriter
from processors.CategoryStructurer import CategoryStructurer
from processors.CategoryImporter import CategoryImporter
from processors.DataImporter import DataImporter
from processors.ExcelWriter import ExcelWriter


def wallet_process_app():
    try:
        data_import = DataImporter(
            _filename="C:\\Users\\Stefano\\Documents\\MEGA\\MegaSync_Pixel\\report_2024-06-23.xls",
            _start_date="2024-01-01",
            _end_date="2024-12-31"
        )
        data_2024 = data_import.get_imported_data()
    except Exception as e:
        print("DataImport(): ".format(e))
        exit()

    try:
        category_import = CategoryImporter()
        wallet_category = category_import.process(data_2024)
    except Exception as e:
        print("CategoryImport() :".format(e))
        exit()

    try:
        category_hierarchy = CategoryStructurer()
        main_category = category_hierarchy.process(wallet_category)
    except Exception as e:
        print("CategoryImport() :".format(e))
        exit()

    excel_writer = ExcelWriter("pandas_text.xlsx", "2024")
    excel_writer.process(main_category,wallet_category)


if __name__ == '__main__':
    wallet_process_app()
