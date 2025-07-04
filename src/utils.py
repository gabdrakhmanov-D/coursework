import datetime
import json
import re
from decimal import Decimal

import requests

import os
from dotenv import load_dotenv
from pandas import DataFrame

load_dotenv()

import pandas as pd
import logging



logger_date = logging.getLogger('get_date')
logger_excel = logging.getLogger('excel_reader')
logger_expenses = logging.getLogger('get_expenses_and_cashback')
logger_top_transact = logging.getLogger('top_transaction')
logger_stock = logging.getLogger('get_stock')
logger_currency_exchange = logging.getLogger('get_currency_exchange')
logger_read_json = logging.getLogger('read_json')
logger_filter_transactions = logging.getLogger('filter_transactions')


def get_date():
    """Функция, которая возвращает строку с датой и временем в формате YYYY-MM-DD HH:MM:SS."""
    logger_date.info('Старт работы функции')
    current_date_time = datetime.datetime.now()
    date_str= current_date_time.strftime("%Y-%m-%d %H:%M:%S")
    logger_date.info('Дата успешно сформирована, возврат даты')
    # return date_str
    return '2021-12-05 15:20:53.'

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


def filter_transactions(list_transactions: list, date_to: str) -> DataFrame:
    """Функция, которая принимает список транзакций и текущую дату в формате YYYY-MM-DD HH:MM:SS.
    Возвращает отфильтрованный по дате ДатаФрейм.
    Фильтрация идет с начала текущего месяца и до текущего дня"""
    pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
    if not re.match(pattern, date_to, flags=0):
        logger_filter_transactions.error(f'Неверный формат даты! Возврат пустого датафрейма {date_to}')
        return pd.DataFrame([])
    if not list_transactions:
        logger_filter_transactions.error('Список транзакций пуст! Возврат пустого датафрейма')
        return pd.DataFrame([])
    logger_filter_transactions.info('Старт работы функции')
    try:
        date_day = int(date_to[8:10])
        date_month = int(date_to[5:7])
        date_year = int(date_to[:4])
        df_transactions = pd.DataFrame(list_transactions)
        df_transactions['Дата операции'] = pd.to_datetime(df_transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S')
        df_date =df_transactions[(df_transactions['Дата операции'].dt.day <= date_day) & (df_transactions['Дата операции'].dt.month == date_month) & (df_transactions['Дата операции'].dt.year== date_year)]
        logger_filter_transactions.info('Успешный возврат отфильтрованного по дате датафрейма')
        return df_date
    except Exception as ex:
        logger_filter_transactions.error(f'Ошибка в работе функции: {ex}')
        return pd.DataFrame([])


def top_transaction(df_top_transactions: DataFrame) -> list:
    """Функция принимает датафрейм и возвращает топ 5 транзакций"""
    logger_top_transact.info('Старт работы функции')
    try:
        if df_top_transactions.empty:
            logger_top_transact.error('Получен пустой датафрейм, возврат пустого списка')
            return []

        logger_top_transact.info('Получен список транзакций')
        df_top = df_top_transactions.sort_values('Сумма платежа', ascending= False, key= abs).iloc[0:5:]
        logger_top_transact.info('Список отсортирован по сумме платежа')
        df_top_day = df_top.sort_values('Дата платежа')
        logger_top_transact.info('Отсортированный список, отсортирован по дате')
        result_top = []
        for index, row in df_top_day.iterrows():
            result_top.append(
                               {
                                "date" : row['Дата платежа'],
                                "amount" : row['Сумма платежа'],
                                "category" : row['Категория'],
                                "description" : row['Описание']
                               }
                              )
        logger_top_transact.info('Список топ 5 транзакций сформирован')
        return result_top

    except Exception as ex:
        print(df_top_transactions)
        logger_top_transact.error(f'Произошла ошибка в работе функции: {ex}')
        return []


def get_expenses_and_cashback(df_date: DataFrame) -> list: #df_date: DataFrame
    """Функция, которая принимает отсортированный по дате датафрейм со списком транзакций, возвращает по каждой карте:
    - последние 4 цифры карты;
    - общая сумма расходов;
    - кешбэк (1 рубль на каждые 100 рублей)."""
    logger_expenses.info('Старт работы функции')

    if df_date.empty:
        logger_excel.error('Ошибка, получен пустой список. Возврат пустого списка')
        return []
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


def read_json_from_file(path_to_file: str = 'C:/Users/rubik/OneDrive/Documents/Pyton/course_work/data/user_settings.json') -> \
tuple[list, list]:
    """Функция для считывания из json-файла списка акций и валют."""
    try:
        logger_read_json.info('Старт работы функции')
        with open(path_to_file) as f:
            data = json.load(f)
            currencies = data.get('user_currencies')
            stocks = data.get('user_stocks')
            logger_read_json.info('Успешное открытие файла и возврат списка акций и валют.')
            return currencies, stocks
    except Exception as ex:
        logger_read_json.error(f'Ошибка в работе функции: {ex}')
        return [], []


def get_stocks_prices(stocks: list) -> list:
    """Функция для получения котировок акций. Принимает список акций и возвращает их стоиость."""
    if not stocks:
        logger_stock.error('Получен пустой список акций, возврат пустого списка!')
        return []

    logger_stock.info('Получен список акций. Старт работы функции')
    url = os.getenv('URL')
    apy_key = os.getenv('API_KEY')
    price_stock = []
    current_stock = (stock for stock in stocks)

    for _ in range(len(stocks)):
        params = {'ticker': next(current_stock)}
        headers = {'X-Api-Key': apy_key}
        response_stock = requests.get(url, headers= headers, params= params)
        if response_stock.status_code != 200:
            logger_stock.error(f'Получена ошибка на запрос: {response_stock}')
            return []
        data_stock = response_stock.json()
        price_stock.append({
                              "stock": data_stock['ticker'],
                              "price": data_stock['price']
                            })
    logger_stock.info('Успешно получен ответ с сайта, возврат списка акций')
    return price_stock


def get_exchange_currency(currencies: list) -> list:
    """Функция для получения курсов валют. Принимает список валют и возвращает курс к рублю."""
    if not currencies:
        logger_currency_exchange.error('Получен пустой список валют, возврат пустого списка!')
        return []

    logger_currency_exchange.info('Получен список валют. Старт работы функции')
    url = os.getenv('URL_CURRENCY')
    apy_key = os.getenv('API_KEY_CURRENCY')
    currency_pairs = [f'{user_currency}RUB' for user_currency in currencies]
    pairs = ','.join(currency_pairs)
    logger_currency_exchange.info('Созданы валютные пары')

    get_params = {
                    'get': 'rates',
                    'pairs': pairs,
                    "key": apy_key
                  }
    response_currency = requests.get(url, params=get_params)

    if response_currency.status_code != 200:
        logger_currency_exchange.error(f'Получена ошибка на запрос: {response_currency}')
        return []

    data_currency =  response_currency.json()
    current_currencies = [
        {
          "currency": currency_pair[:3],
          "rate": data_currency['data'][currency_pair]
        }
        for currency_pair in currency_pairs]

    logger_currency_exchange.info('Успешный возврат курсов валют')
    return current_currencies
