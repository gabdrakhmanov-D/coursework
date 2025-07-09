import json
from unittest import mock
from unittest.mock import patch, mock_open
import pandas as pd
import pytest

from src.reports import write_to_file, spending_by_category


def test_write_to_file():
    """Тестирование работы декоратора без указания имени файла"""
    with (patch("builtins.open", new_callable=mock_open) as mock_data,
        patch('json.dump')):
        @write_to_file()
        def get_dataframe():
            df = pd.DataFrame({'Yes': [50, 21], 'No': [131, 2]})
            return df

        result = get_dataframe()
    mock_data.assert_called_once_with('report_by_category.json', 'w', encoding='utf-8')


def test_write_to_file_test():
    """Тестирование работы декоратора с указанием имени файла 'test'"""
    with (patch("builtins.open", new_callable=mock_open) as mock_data,
        patch('json.dump')):
        @write_to_file('test')
        def get_dataframe():
            df = pd.DataFrame({'Yes': [50, 21], 'No': [131, 2]})
            return df

        result = get_dataframe()
    mock_data.assert_called_once_with('test.json', 'w', encoding='utf-8')


def test_write_to_file_empty_df():
    """Тестирование работы декоратора при поступлении пустого датафрейма"""
    with (patch("builtins.open", new_callable=mock_open) as mock_data,
        patch('json.dump')):
        @write_to_file('test')
        def get_dataframe():
            df = pd.DataFrame()
            return df
        result = get_dataframe()
    mock_data.assert_not_called()


#тесты для функции spending_by_category
@pytest.mark.parametrize('expected', [
                                        [{'Дата операции': '01.12.2021',
                                          'Дата платежа': '01.12.2021',
                                          'Категория': 'Супермаркеты',
                                          'Номер карты': '*7197',
                                          'Описание': 'Колхоз',
                                          'Сумма операции': -160.89,
                                          'Сумма платежа': -160.89},
                                         {'Дата операции': '01.11.2021',
                                          'Дата платежа': '01.11.2021',
                                          'Категория': 'Супермаркеты',
                                          'Номер карты': '*7197',
                                          'Описание': 'Колхоз',
                                          'Сумма операции': -64.0,
                                          'Сумма платежа': -64.0},
                                         {'Дата операции': '02.10.2021',
                                          'Дата платежа': '02.10.2021',
                                          'Категория': 'Супермаркеты',
                                          'Номер карты': '*7197',
                                          'Описание': 'Вези меня',
                                          'Сумма операции': -118.12,
                                          'Сумма платежа': -118.12}]])
def test_spending_by_category(return_dataframe_for_spending_by_category, expected):
    """Тестирование успешной работы функции"""
    result = spending_by_category(return_dataframe_for_spending_by_category,
                                  "Супермаркеты",
                                  "31.12.2021").to_dict('records')
    assert result == expected