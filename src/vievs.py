import json
import logging
from src.utils import get_date, read_json_from_file, excel_file_reader, top_transaction, filter_transactions, \
    get_expenses_and_cashback, get_stocks_prices, get_exchange_currency

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s',
                    filename='C:/Users/rubik/OneDrive/Documents/Pyton/course_work/logs/application.log',
                    filemode='w',
                    encoding='utf-8')

logger_user_transactions = logging.getLogger('user_transactions')


def get_user_transactions(current_date: str) -> json:
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
        greeting_value = 'Доброе утро!'
    elif 18 > int(current_date[11:13]) > 12:
        greeting_value = 'Добрый день!'
    elif 24 > int(current_date[11:13]) > 18:
        greeting_value = 'Добрый вечер!'
    else:
        greeting_value = 'Доброй ночи'

    path_to_json_user_parameters = 'C:/Users/rubik/OneDrive/Documents/Pyton/course_work/data/user_settings.json'
    path_to_user_excel_transactions = 'C:/Users/rubik/OneDrive/Documents/Pyton/course_work/data/operations.xlsx'

    user_transactions_from_excel = excel_file_reader(path_to_user_excel_transactions) # получение транзакций из excel файла
    filtered_df = filter_transactions(user_transactions_from_excel, current_date) # получение отфильтрованного по дате датафрейма
    if filtered_df.empty:
        raise Exception('Ошибка в работе программы, не получены данные о транзакциях')

    user_currency, user_stocks = read_json_from_file(path_to_json_user_parameters) # получаем из json файла список акций и валют
    top_user_transactions = top_transaction(filtered_df) # получаем топ 5 транзакций
    user_expenses_and_cashback = get_expenses_and_cashback(filtered_df) # получаем расходы и инфо по каждой карте
    user_stocks_prices = get_stocks_prices(user_stocks) # получаем цену акций
    user_currency_exchange = get_exchange_currency(user_currency) # получаем курс валют

    result = {
        "greeting": greeting_value,
        "cards" : user_expenses_and_cashback,
        "top_transactions" : top_user_transactions,
        "currency_rates" : user_currency_exchange,
        "stock_prices" : user_stocks_prices
    }
    return json.dumps(result, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    print(get_user_transactions(get_date()))
