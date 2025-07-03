import datetime
from decimal import Decimal
from math import ceil

import pandas as pd
import logging

from pandas.core.interchange.dataframe_protocol import DataFrame

logger_date = logging.getLogger('get_date')
logger_excel = logging.getLogger('excel_reader')
logger_expenses = logging.getLogger('get_expenses_and_cashback')


def get_date():
    """Функция, которая возвращает строку с датой и временем в формате YYYY-MM-DD HH:MM:SS."""
    logger_date.info('Старт работы функции')
    current_date_time = datetime.datetime.now()
    date_str= current_date_time.strftime("%Y-%m-%d %H:%M:%S")
    logger_date.info('Дата успешно сформирована, возврат даты')
    return date_str


def excel_file_reader(path_to_file: str = 'C:/Users/rubik/OneDrive/Documents/Pyton/course_work/data/operations.xlsx') -> list:
    """Функция для считывания финансовых операций из Excel, принимает путь к файлу Excel в качестве аргумента.
    Возвращает список словарей с транзакциями."""
    logger_excel.info('Старт работы функции.')
    try:
        excel_df = pd.read_excel(path_to_file).fillna(0)
        logger_excel.info('Успешное чтение файла, возврат содержимого')
        return excel_df.to_dict('records')
    except Exception as ex:
        logger_excel.error(f'Ошибка чтения файла: {ex}.\nВозврат пустого списка.')
        return []

#list_transactions: list

def get_info(date_to: str):
    """Функция, которая принимает список транзакций, период даты и возвращает по каждой карте:
- последние 4 цифры карты;
- общая сумма расходов;
- кешбэк (1 рубль на каждые 100 рублей).
- Топ-5 транзакций по сумме платежа."""
    date_day = int(date_to[8:10])
    date_month = int(date_to[5:7])
    date_year = int(date_to[:4])
    list_transactions = excel_file_reader()
    df_transactions = pd.DataFrame(list_transactions)
    df_transactions['Дата операции'] = pd.to_datetime(df_transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    df_date =df_transactions[(df_transactions['Дата операции'].dt.day <= date_day) & (df_transactions['Дата операции'].dt.month == date_month) & (df_transactions['Дата операции'].dt.year== date_year)]

    # top_transactions = df_date.groupby('Дата платежа').apply(lambda x: max(x['Сумма платежа']))
    top_transactions = df_date.sort_values(['Сумма платежа'])

    # print(top_transactions)
    return df_date
# get_info('2021-12-05')

def get_expenses_and_cashback() -> list: #df_date: DataFrame
    """Функция, которая принимает отсортированный по дате датафрейм со списком транзакций, возвращает по каждой карте:
    - последние 4 цифры карты;
    - общая сумма расходов;
    - кешбэк (1 рубль на каждые 100 рублей)."""
    logger_expenses.info('Старт работы функции')
    df_date = get_info('2021-12-10')
    if df_date:
        try:
            logger_expenses.info('Получен дата фрейм, началась обработка')
            expenses = df_date[df_date['Сумма платежа'] < 0]
            result_df = expenses.groupby(by='Номер карты').agg({'Сумма платежа': 'sum'}).reset_index()
            list_expenses = []
            for index, row in result_df.iterrows():
                expense_on_the_card = Decimal(abs(row['Сумма платежа'])).quantize(Decimal("1.00"))
                cashback = Decimal(expense_on_the_card/100).quantize(Decimal("1.00"))
                list_expenses.append({
                    "last_digits": f'{row['Номер карты'][1:]}',
                    "total_spent": f'{expense_on_the_card}',
                    "cashback": f'{cashback}'
                })
                logger_excel.info('Список успешно сформирован, возврат списка')
            return list_expenses
        except Exception as ex:
            logger_excel.error(f'Ошибка работы функции: {ex}')
            return []
    else:
        logger_excel.error('Ошибка, получен пустой список. Возврат пустого списка')
        return []

get_expenses_and_cashback()
# "cards": [
#     {
#       "last_digits": "5814",
#       "total_spent": 1262.00,
#       "cashback": 12.62
#     },
#     {
#       "last_digits": "7512",
#       "total_spent": 7.94,
#       "cashback": 0.08
#     }
#   ],