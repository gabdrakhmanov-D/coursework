from unittest.mock import patch

import pandas as pd
import pytest

from src.views import get_user_operations


@pytest.mark.parametrize(
    "result, example_df",
    [
        (
            (
                "{\n"
                '    "greeting": "Доброе утро!",\n'
                '    "cards": [\n'
                '        "*1234"\n'
                "    ],\n"
                '    "top_transactions": [\n'
                '        "top_user_transactions"\n'
                "    ],\n"
                '    "currency_rates": [\n'
                '        "user_currency_exchange"\n'
                "    ],\n"
                '    "stock_prices": [\n'
                '        "user_stocks_prices"\n'
                "    ]\n"
                "}"
            ),
            pd.DataFrame(({"cards": ["1234"], "amount": ["1000"]})),
        )
    ],
)
def test_get_user_operations(result, example_df):
    """Тестирование успешной работы функции"""
    with (
        patch("src.views.excel_file_reader"),
        patch("src.views.filter_transactions", return_value=example_df),
        patch("src.views.top_transaction", return_value=["top_user_transactions"]),
        patch("src.views.get_expenses_and_cashback", return_value=["*1234"]),
        patch("src.views.get_stocks_prices", return_value=["user_stocks_prices"]),
        patch("src.views.get_exchange_currency", return_value=["user_currency_exchange"]),
    ):
        assert get_user_operations("2006-07-05 10:34:09") == result


@pytest.mark.parametrize(
    "result, example_df",
    [
        (
            (
                "{\n"
                '    "greeting": "Доброе утро!",\n'
                '    "cards": "Данные не получены",\n'
                '    "top_transactions": "Данные не получены",\n'
                '    "currency_rates": [\n'
                '        "user_currency_exchange"\n'
                "    ],\n"
                '    "stock_prices": [\n'
                '        "user_stocks_prices"\n'
                "    ]\n"
                "}"
            ),
            pd.DataFrame(({"cards": ["1234"], "amount": ["1000"]})),
        )
    ],
)
def test_get_user_operations_no_excel(result, example_df):
    """Тестирование ошибки чтения excel файла"""
    with (
        patch("src.views.excel_file_reader", return_value=[]),
        patch("src.views.filter_transactions", return_value=example_df),
        patch("src.views.top_transaction", return_value=["top_user_transactions"]),
        patch("src.views.get_expenses_and_cashback", return_value=["*1234"]),
        patch("src.views.get_stocks_prices", return_value=["user_stocks_prices"]),
        patch("src.views.get_exchange_currency", return_value=["user_currency_exchange"]),
    ):
        assert get_user_operations("2006-07-05 10:34:09") == result


@pytest.mark.parametrize(
    "result, example_df",
    [
        (
            (
                "{\n"
                '    "greeting": "Доброй ночи!",\n'
                '    "cards": "Данные не получены",\n'
                '    "top_transactions": "Данные не получены",\n'
                '    "currency_rates": [\n'
                '        "user_currency_exchange"\n'
                "    ],\n"
                '    "stock_prices": [\n'
                '        "user_stocks_prices"\n'
                "    ]\n"
                "}"
            ),
            pd.DataFrame(({"cards": ["1234"], "amount": ["1000"]})),
        )
    ],
)
def test_get_user_operations_no_df(result, example_df):
    """Тестирование ошибки получения датафрейма"""
    with (
        patch("src.views.excel_file_reader", return_value=["excel_data"]),
        patch("src.views.filter_transactions"),
        patch("src.views.top_transaction", return_value=["top_user_transactions"]),
        patch("src.views.get_expenses_and_cashback", return_value=["*1234"]),
        patch("src.views.get_stocks_prices", return_value=["user_stocks_prices"]),
        patch("src.views.get_exchange_currency", return_value=["user_currency_exchange"]),
    ):
        assert get_user_operations("2006-07-05 00:34:09") == result


@pytest.mark.parametrize(
    "result, example_df",
    [
        (
            (
                "{\n"
                '    "greeting": "Добрый вечер!",\n'
                '    "cards": [\n'
                '        "*1234"\n'
                "    ],\n"
                '    "top_transactions": [\n'
                '        "top_user_transactions"\n'
                "    ],\n"
                '    "currency_rates": "Не выбрана валюта для получения курса",\n'
                '    "stock_prices": "Не выбраны акции для получения цены"\n'
                "}"
            ),
            pd.DataFrame(({"cards": ["1234"], "amount": ["1000"]})),
        )
    ],
)
def test_get_user_operations_no_json(result, example_df):
    """Тестирование ошибки чтения json и получения списка акций и валют"""
    with (
        patch("src.views.excel_file_reader", return_value=["excel_data"]),
        patch("src.views.filter_transactions", return_value=example_df),
        patch("src.views.top_transaction", return_value=["top_user_transactions"]),
        patch("src.views.get_expenses_and_cashback", return_value=["*1234"]),
        patch("src.views.read_json_from_file", return_value=([], [])),
        patch("src.views.get_stocks_prices", return_value=["user_stocks_prices"]),
        patch("src.views.get_exchange_currency", return_value=["user_currency_exchange"]),
    ):
        assert get_user_operations("2006-07-05 18:34:09") == result


@pytest.mark.parametrize(
    "result, example_df",
    [
        (
            (
                "{\n"
                '    "greeting": "Добрый день!",\n'
                '    "cards": [\n'
                '        "*1234"\n'
                "    ],\n"
                '    "top_transactions": [\n'
                '        "top_user_transactions"\n'
                "    ],\n"
                '    "currency_rates": [\n'
                '        "user_currency_exchange"\n'
                "    ],\n"
                '    "stock_prices": "Не выбраны акции для получения цены"\n'
                "}"
            ),
            pd.DataFrame(({"cards": ["1234"], "amount": ["1000"]})),
        )
    ],
)
def test_get_user_operations_no_stock(result, example_df):
    """Тестирование случая когда нет списка валют"""
    with (
        patch("src.views.excel_file_reader", return_value=["excel_data"]),
        patch("src.views.filter_transactions", return_value=example_df),
        patch("src.views.top_transaction", return_value=["top_user_transactions"]),
        patch("src.views.get_expenses_and_cashback", return_value=["*1234"]),
        patch("src.views.read_json_from_file", return_value=(["EUR"], [])),
        patch("src.views.get_stocks_prices", return_value=["user_stocks_prices"]),
        patch("src.views.get_exchange_currency", return_value=["user_currency_exchange"]),
    ):
        assert get_user_operations("2006-07-05 13:34:09") == result


@pytest.mark.parametrize(
    "result, example_df",
    [
        (
            (
                "{\n"
                '    "greeting": "Доброе утро!",\n'
                '    "cards": [\n'
                '        "*1234"\n'
                "    ],\n"
                '    "top_transactions": [\n'
                '        "top_user_transactions"\n'
                "    ],\n"
                '    "currency_rates": "Не выбрана валюта для получения курса",\n'
                '    "stock_prices": [\n'
                '        "user_stocks_prices"\n'
                "    ]\n"
                "}"
            ),
            pd.DataFrame(({"cards": ["1234"], "amount": ["1000"]})),
        )
    ],
)
def test_get_user_operations_no_currency(result, example_df):
    """Тестирование случая когда нет списка акций"""
    with (
        patch("src.views.excel_file_reader", return_value=["excel_data"]),
        patch("src.views.filter_transactions", return_value=example_df),
        patch("src.views.top_transaction", return_value=["top_user_transactions"]),
        patch("src.views.get_expenses_and_cashback", return_value=["*1234"]),
        patch("src.views.read_json_from_file", return_value=([], ["AMZN"])),
        patch("src.views.get_stocks_prices", return_value=["user_stocks_prices"]),
        patch("src.views.get_exchange_currency", return_value=["user_currency_exchange"]),
    ):
        assert get_user_operations("2006-07-05 10:34:09") == result
