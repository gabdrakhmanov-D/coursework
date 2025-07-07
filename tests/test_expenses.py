from unittest.mock import patch

import pandas as pd
import pytest

from src.utils import get_expenses_and_cashback


@pytest.mark.parametrize(
    "expected",
    [
        [
            {"last_digits": "1234", "total_spent": "1071.00", "cashback": "10.71"},
            {"last_digits": "7197", "total_spent": "343.01", "cashback": "3.43"},
        ]
    ],
)
def test_get_expenses_and_cashback(return_sorted_dataframe, expected):
    """Тестирование успешной работы функции"""
    assert get_expenses_and_cashback(return_sorted_dataframe) == expected


def test_get_expenses_and_cashback_empty_df():
    """Тестирование получения пустого датафрейма"""
    empty_df = pd.DataFrame()
    assert get_expenses_and_cashback(empty_df) == []


def test_get_expenses_and_cashback_error(return_sorted_dataframe):
    """Тестирование случая ошибки при выполнении функции"""
    with patch("pandas.DataFrame.groupby") as mock_group:
        mock_group.return_value = Exception
        assert get_expenses_and_cashback(return_sorted_dataframe) == []
        mock_group.assert_called_once_with(by="Номер карты")
