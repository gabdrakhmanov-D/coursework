import datetime
import json
from decimal import Decimal
from locale import currency

import requests

import os
from dotenv import load_dotenv
load_dotenv()

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


def get_json_from_file(path_to_file: str = 'C:/Users/rubik/OneDrive/Documents/Pyton/course_work/data/user_settings.json') -> json:
    """Функция для считывания json из файла"""
    with open(path_to_file) as f:
        data = json.load(f)
        return data


def get_list_of_stocks() -> tuple[list, list]:
    """Функция для получения из json списка акций и выбранных пользователем валют."""

    data = get_json_from_file()
    currencies = data.get('user_currencies')
    stocks = data.get('user_stocks')
    return currencies, stocks

def get_stocks_prices():
    """Функция для получения котировок акций."""
    url = os.getenv('URL')
    apy_key = os.getenv('API_KEY')
    currencies, stocks = get_list_of_stocks()
    price_stock = []
    current_currencies = []
    current_stock = (stock for stock in stocks)
    current_currency = (user_currency for user_currency in currencies)

    for _ in range(len(stocks)):
        get_params = {
                        'function': 'GLOBAL_QUOTE',
                        'symbol': next(current_stock),
                        "apikey": apy_key
                      }

        r = requests.get(url, params=get_params)
        data_stock = r.json()
        price_stock.append({
                              "stock": data_stock['Global Quote']['01. symbol'],
                              "price": data_stock['Global Quote']['05. price']
                            })
        # {
        #     "Global Quote": {
        #         "01. symbol": "IBM",
        #         "02. open": "290.0000",
        #         "03. high": "290.1900",
        #         "04. low": "286.9000",
        #         "05. price": "287.6500",
        #         "06. volume": "3257515",
        #         "07. latest trading day": "2025-07-02",
        #         "08. previous close": "291.2000",
        #         "09. change": "-3.5500",
        #         "10. change percent": "-1.2191%"
        #     }
        # }

    for _ in range(len(currencies)):
        get_params = {
                        'function': 'CURRENCY_EXCHANGE_RATE',
                        'from_currency': 'RUB',
                        'to_currency': next(current_currency),
                        "apikey": apy_key
                      }
        r = requests.get(url, params=get_params)
        data_currency = r.json()
        current_currencies.append({
                              "currency": data_currency['Realtime Currency Exchange Rate']['3. To_Currency Code'],
                              "rate": data_currency['Realtime Currency Exchange Rate']['5. Exchange Rate']
                            })
    print(price_stock)
    print(current_currencies)

get_stocks_prices()
# {
#     "Realtime Currency Exchange Rate": {
#         "1. From_Currency Code": "USD",
#         "2. From_Currency Name": "United States Dollar",
#         "3. To_Currency Code": "JPY",
#         "4. To_Currency Name": "Japanese Yen",
#         "5. Exchange Rate": "145.04100000",
#         "6. Last Refreshed": "2025-07-03 18:40:45",
#         "7. Time Zone": "UTC",
#         "8. Bid Price": "145.03910000",
#         "9. Ask Price": "145.04640000"
#     }
# }