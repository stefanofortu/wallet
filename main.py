from Category_List import CategoryResults, AllCategory
from ExpenseHandler import ExpenseHandler
from WalletChecker import WalletChecker





# def get_results_group_by_level(all_category_results, expense_hierarchy, level) -> CategoryResults:
#     if not isinstance(all_category_results, CategoryResults):
#         print("wrong input - results")
#         exit()
#
#     if not isinstance(expense_hierarchy, ExpenseHandler):
#         print("wrong input - expense_hierarchy")
#         exit()
#
#     if not isinstance(level, int):
#         if level <= 0 or level > 3:
#             print("wrong input - level")
#             exit()
#
#     category_list = expense_hierarchy.get_level_category_list(level)
#     for cat in category_list:
#         print(cat.name, cat.child_list)
#         amount = 0
#         for child_cat in cat.child_list:
#             amount += all_category_results[child_cat]
#     exit()


if __name__ == '__main__':
    expense_handler = ExpenseHandler()

    wallet_checker = WalletChecker()
    wallet_checker.select_personal_accounts()

    data = wallet_checker.get_data()

    try:
        data_2024 = WalletChecker.get_time_filtered_data(data=data, start_date="2024-01-01", end_date="2024-05-31")
    except Exception as error:
        print("An exception occurred:", error)
        print("Error: get_filtered_data()")
        exit()

    try:
        data_2024_cat = WalletChecker.get_data_by_single_category(data=data_2024, category="Placeholder")
    except Exception as error:
        print("An exception occurred:", error)
        print("Error: get_filtered_data()")
        exit()

    print(data_2024_cat[["account", "category", "amount", "date"]])
    all_category = AllCategory()
    all_amounts = CategoryResults()

    for cat in all_category.all_category:
        try:
            amount = WalletChecker.get_amount_by_category(data=data_2024, category=cat)
            all_amounts.append(cat, amount)
        except Exception as error:
            print("Error: get_filtered_data()", error)
            exit()

    first_level_results = CategoryResults()

    print(all_amounts)

    #
    #get_results_group_by_level(results, expense_handler, 1)

    #import xlsxwriter
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
