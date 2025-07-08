import json
from unittest import mock
from unittest.mock import patch, mock_open
import pandas as pd
from src.reports import write_to_file


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