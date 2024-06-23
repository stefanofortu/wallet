import xlsxwriter
from CategoryStructurer import CategoryStructurer
from CategoryImporter import CategoryImporter
from DataImport import DataImport


def wallet_process_app():
    try:
        data_import = DataImport(
            _filename="C:\\Users\\Stefano\\Documents\\MEGA\\MegaSync_Pixel\\report_2024-06-23.xls",
            _start_date="2024-01-01",
            _end_date="2024-07-31"
        )
    except Exception as e:
        print("main: DataImport() creation")
        print('An exception occurred: {}'.format(e))
        exit()

    data_2024 = data_import.get_imported_data()

    # wallet_checker = WalletChecker()
    # wallet_checker.select_personal_accounts()

    # data = wallet_checker.get_data()

    try:
        category_import = CategoryImporter()
        wallet_category = category_import.process(data_2024)
    except Exception as error:
        print("CategoryImport():", error)
        exit()

    #try:
    category_hierarchy = CategoryStructurer()
    all_category = category_hierarchy.process(wallet_category)
    #except Exception as error:
    #    print("CategoryHierarchy():", error)
    #    exit()

    print(all_category)
    exit()







    # Workbook() takes one, non-optional, argument
    # which is the filename that we want to create.
    workbook = xlsxwriter.Workbook('hello.xlsx')

    # The workbook object is then used to add new
    # worksheet via the add_worksheet() method.
    worksheet = workbook.add_worksheet()

    # Use the worksheet object to write
    # data via the write() method.
    worksheet.write('A1', 'Hello..')
    worksheet.write('B1', 'Geeks')
    worksheet.write('C1', 'For')
    worksheet.write('D1', 'Geeks')

    # Finally, close the Excel file
    # via the close() method.
    workbook.close()

    # print(data_2024_spesa['amount'].sum())
    # print(data_2024_salary["date"][0].year)
    # print(data_2024_salary["date"][0].month)
    # print(data_2024_salary.columns.tolist())
    exit()


if __name__ == '__main__':
    wallet_process_app()
