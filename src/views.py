import json
import logging

from config import PATH_TO_LOGGER, PATH_TO_OPERATIONS, PATH_TO_USER_SETTINGS
from src.utils import (excel_file_reader, filter_transactions, get_exchange_currency, get_expenses_and_cashback,
                       get_stocks_prices, read_json_from_file, top_transaction)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s",
    filename=PATH_TO_LOGGER,
    filemode="w",
    encoding="utf-8",
)

logger_user_operations = logging.getLogger("user_transactions")


def get_user_operations(current_date: str) -> json:
    """Функция принимает текущую дату и возвращает:
    Приветствие в формате
    "???", где ??? — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи» в зависимости от текущего времени.
    По каждой карте:
    - последние 4 цифры карты;
    - общая сумма расходов;
    - кешбэк (1 рубль на каждые 100 рублей).
    - Топ-5 транзакций по сумме платежа.
    - Курс валют.
    - Стоимость акций из S&P500."""

    if 12 > int(current_date[11:13]) > 6:
        greeting_value = "Доброе утро!"
    elif 18 > int(current_date[11:13]) >= 12:
        greeting_value = "Добрый день!"
    elif 24 > int(current_date[11:13]) >= 18:
        greeting_value = "Добрый вечер!"
    else:
        greeting_value = "Доброй ночи!"

    path_to_json_user_parameters = PATH_TO_USER_SETTINGS
    path_to_user_excel_transactions = PATH_TO_OPERATIONS

    user_transactions_from_excel = excel_file_reader(
        path_to_user_excel_transactions
    )  # получение транзакций из excel файла
    if not user_transactions_from_excel:
        user_expenses_and_cashback, top_user_transactions = "Данные не получены", "Данные не получены"
        user_currency, user_stocks = read_json_from_file(path_to_json_user_parameters)
        if not user_currency and not user_stocks:
            user_currency_exchange = "Не выбрана валюта для получения курса"
            user_stocks_prices = "Не выбраны акции для получения цены"
        elif not user_currency:
            user_currency_exchange = "Не выбрана валюта для получения курса"
            user_stocks_prices = get_stocks_prices(user_stocks)  # получаем цену акций
        elif not user_stocks:
            user_stocks_prices = "Не выбраны акции для получения цены"
            user_currency_exchange = get_exchange_currency(user_currency)  # получаем курс валют
        else:
            user_stocks_prices = get_stocks_prices(user_stocks)  # получаем цену акций
            user_currency_exchange = get_exchange_currency(user_currency)  # получаем курс валют
        result = {
            "greeting": greeting_value,
            "cards": user_expenses_and_cashback,
            "top_transactions": top_user_transactions,
            "currency_rates": user_currency_exchange,
            "stock_prices": user_stocks_prices,
        }
        return json.dumps(result, indent=4, ensure_ascii=False)

    filtered_df = filter_transactions(
        user_transactions_from_excel, current_date
    )  # получение отфильтрованного по дате датафрейма
    if filtered_df.empty:
        user_expenses_and_cashback, top_user_transactions = "Данные не получены", "Данные не получены"
        user_currency, user_stocks = read_json_from_file(path_to_json_user_parameters)
        if not user_currency and not user_stocks:
            user_currency_exchange = "Не выбрана валюта для получения курса"
            user_stocks_prices = "Не выбраны акции для получения цены"
        elif not user_currency:
            user_currency_exchange = "Не выбрана валюта для получения курса"
            user_stocks_prices = get_stocks_prices(user_stocks)  # получаем цену акций
        elif not user_stocks:
            user_stocks_prices = "Не выбраны акции для получения цены"
            user_currency_exchange = get_exchange_currency(user_currency)  # получаем курс валют
        else:
            user_stocks_prices = get_stocks_prices(user_stocks)  # получаем цену акций
            user_currency_exchange = get_exchange_currency(user_currency)  # получаем курс валют
        result = {
            "greeting": greeting_value,
            "cards": user_expenses_and_cashback,
            "top_transactions": top_user_transactions,
            "currency_rates": user_currency_exchange,
            "stock_prices": user_stocks_prices,
        }
        return json.dumps(result, indent=4, ensure_ascii=False)

    top_user_transactions = top_transaction(filtered_df)  # получаем топ 5 транзакций
    user_expenses_and_cashback = get_expenses_and_cashback(filtered_df)  # получаем расходы и инфо по каждой карте
    user_currency, user_stocks = read_json_from_file(
        path_to_json_user_parameters
    )  # получаем из json файла список акций и валют
    if not user_currency and not user_stocks:
        user_currency_exchange = "Не выбрана валюта для получения курса"
        user_stocks_prices = "Не выбраны акции для получения цены"
    elif not user_currency:
        user_currency_exchange = "Не выбрана валюта для получения курса"
        user_stocks_prices = get_stocks_prices(user_stocks)  # получаем цену акций
    elif not user_stocks:
        user_stocks_prices = "Не выбраны акции для получения цены"
        user_currency_exchange = get_exchange_currency(user_currency)  # получаем курс валют
    else:
        user_stocks_prices = get_stocks_prices(user_stocks)  # получаем цену акций
        user_currency_exchange = get_exchange_currency(user_currency)  # получаем курс валют

    result = {
        "greeting": greeting_value,
        "cards": user_expenses_and_cashback,
        "top_transactions": top_user_transactions,
        "currency_rates": user_currency_exchange,
        "stock_prices": user_stocks_prices,
    }
    return json.dumps(result, indent=4, ensure_ascii=False)
