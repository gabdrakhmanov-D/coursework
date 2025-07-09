import logging

import pandas as pd
from config import PATH_TO_OPERATIONS, PATH_TO_LOGGER
from src.reports import write_to_file, spending_by_category
from src.services import search_for_transfers
from src.utils import get_date, excel_file_reader
from src.views import get_user_operations

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s",
    filename=PATH_TO_LOGGER,
    filemode="w",
    encoding="utf-8",
)


def start_functionality():
    """Функция для получения результата всех реализованных в проекте функциональностей."""
    path_to_user_excel_transactions = PATH_TO_OPERATIONS
    current_date = get_date()
    list_transactions = excel_file_reader(path_to_user_excel_transactions)
    df_transactions = pd.DataFrame(list_transactions)
    user_operations = get_user_operations(current_date)
    user_transfers = search_for_transfers(list_transactions)
    report_date = input('Введите конечную дату формирования отчета в формате: dd.mm.yyyy.\n')
    selected_category = input('Введите категорию для формирования отчета, например: "Транспорт".\n')
    need_report_file_name = input('''Хотите назвать файл отчета?
По умолчанию файл будет назван report_by_category. Да/Нет\n''').capitalize()
    if need_report_file_name == 'Да':
        report_file_name = input('Введите название файла, для сохранения отчета\n')
    else:
        report_file_name = None
    write_to_file(report_file_name)(spending_by_category)(df_transactions, selected_category, report_date)
    return user_operations, user_transfers

if __name__ == '__main__':
    start_functionality()