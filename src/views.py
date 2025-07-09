import json
import logging

from config import PATH_TO_LOGGER, PATH_TO_OPERATIONS, PATH_TO_USER_SETTINGS
from src.utils import (excel_file_reader, filter_transactions, get_exchange_currency, get_expenses_and_cashback,
                       get_stocks_prices, read_json_from_file, top_transaction)

logger_user_operations = logging.getLogger("user_operations")


def get_user_operations(current_date: str) -> str:
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
    logger_user_operations.info('Старт работы функции')
    if 12 > int(current_date[11:13]) > 6:
        greeting_value = "Доброе утро!"
    elif 18 > int(current_date[11:13]) >= 12:
        greeting_value = "Добрый день!"
    elif 24 > int(current_date[11:13]) >= 18:
        greeting_value = "Добрый вечер!"
    else:
        greeting_value = "Доброй ночи!"
    logger_user_operations.info(f'Получено значение: {greeting_value}')

    user_transactions_from_excel = excel_file_reader(PATH_TO_OPERATIONS)  # получение транзакций из excel файла
    if not user_transactions_from_excel:
        logger_user_operations.error('Не получен список транзакций из excel файла!')
        user_expenses_and_cashback, top_user_transactions = "Данные не получены", "Данные не получены"
        user_currency, user_stocks = read_json_from_file(PATH_TO_USER_SETTINGS)
        if not user_currency and not user_stocks:
            logger_user_operations.error('Не получен список акций и валют!')
            user_currency_exchange = "Не выбрана валюта для получения курса"
            user_stocks_prices = "Не выбраны акции для получения цены"
        elif not user_currency:
            logger_user_operations.error('Не получен список валют!')
            user_currency_exchange = "Не выбрана валюта для получения курса"
            logger_user_operations.info('Получаем цену акций')
            user_stocks_prices = get_stocks_prices(user_stocks)  # получаем цену акций
        elif not user_stocks:
            logger_user_operations.error('Не получен список акций!')
            user_stocks_prices = "Не выбраны акции для получения цены"
            logger_user_operations.info('Получаем курс валют')
            user_currency_exchange = get_exchange_currency(user_currency)  # получаем курс валют
        else:
            logger_user_operations.info('Получаем цену акций и курс валют')
            user_stocks_prices = get_stocks_prices(user_stocks)  # получаем цену акций
            user_currency_exchange = get_exchange_currency(user_currency)  # получаем курс валют
        result = {
            "greeting": greeting_value,
            "cards": user_expenses_and_cashback,
            "top_transactions": top_user_transactions,
            "currency_rates": user_currency_exchange,
            "stock_prices": user_stocks_prices,
        }
        logger_user_operations.info('Возврат результата.')
        return json.dumps(result, indent=4, ensure_ascii=False)

    filtered_df = filter_transactions(
        user_transactions_from_excel, current_date
    )  # получение отфильтрованного по дате датафрейма
    if filtered_df.empty:
        logger_user_operations.error('Не получен отфильтрованный датафрейм!')
        user_expenses_and_cashback, top_user_transactions = "Данные не получены", "Данные не получены"
        user_currency, user_stocks = read_json_from_file(PATH_TO_USER_SETTINGS)
        if not user_currency and not user_stocks:
            logger_user_operations.error('Не получен список акций и валют!')
            user_currency_exchange = "Не выбрана валюта для получения курса"
            user_stocks_prices = "Не выбраны акции для получения цены"
        elif not user_currency:
            logger_user_operations.error('Не получен список валют!')
            user_currency_exchange = "Не выбрана валюта для получения курса"
            logger_user_operations.info('Получаем цену акций')
            user_stocks_prices = get_stocks_prices(user_stocks)  # получаем цену акций
        elif not user_stocks:
            logger_user_operations.error('Не получен список акций!')
            user_stocks_prices = "Не выбраны акции для получения цены"
            logger_user_operations.info('Получаем курс валют')
            user_currency_exchange = get_exchange_currency(user_currency)  # получаем курс валют
        else:
            logger_user_operations.info('Получаем цену акций и курс валют')
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
    user_currency, user_stocks = read_json_from_file(PATH_TO_USER_SETTINGS)  # получаем из json файла список акций и валют
    if not user_currency and not user_stocks:
        logger_user_operations.error('Не получен список акций и валют!')
        user_currency_exchange = "Не выбрана валюта для получения курса"
        user_stocks_prices = "Не выбраны акции для получения цены"
    elif not user_currency:
        logger_user_operations.error('Не получен список валют!')
        user_currency_exchange = "Не выбрана валюта для получения курса"
        logger_user_operations.info('Получаем цену акций')
        user_stocks_prices = get_stocks_prices(user_stocks)  # получаем цену акций
    elif not user_stocks:
        logger_user_operations.error('Не получен список акций!')
        user_stocks_prices = "Не выбраны акции для получения цены"
        logger_user_operations.info('Получаем курс валют')
        user_currency_exchange = get_exchange_currency(user_currency)  # получаем курс валют
    else:
        logger_user_operations.info('Получаем цену акций и курс валют')
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
