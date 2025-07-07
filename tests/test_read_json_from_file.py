from unittest import mock
from unittest.mock import patch

import pytest

from src.utils import read_json_from_file


def test_read_json_from_file_str():
    """Тестирование случая когда в JSON файле строка"""
    with patch(
        "builtins.open",
        new_callable=mock.mock_open,
        read_data='"user_currencies": ["USD", "EUR"]',
    ) as mock_data:
        assert read_json_from_file("test") == ([], [])
        # Проверяем, что функция open была вызвана правильно
        mock_data.assert_called_once_with("test")


def test_read_json_from_file_empty_list():
    """Тестирование случая когда JSON файл пустой"""
    with patch("builtins.open", new_callable=mock.mock_open, read_data="") as mock_data:
        assert read_json_from_file("test") == ([], [])
        mock_data.assert_called_once_with("test")


def test_read_json_from_file_not_found():
    """Тестирования случая когда файл не найден"""
    with patch("builtins.open", side_effect=FileNotFoundError) as mock_data:
        assert read_json_from_file("test") == ([], [])
        mock_data.assert_called_once_with("test")


@pytest.mark.parametrize(
    "expected, test_list",
    [((["USD", "EUR"], ["AAPL", "AMZN"]), '{"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN"]}')],
)
def test_read_json_from_file_success(test_list, expected):
    """Тестирование успешного чтения файла"""
    with patch("builtins.open", new_callable=mock.mock_open, read_data=f"{test_list}") as mock_data:
        assert read_json_from_file("test") == expected
        mock_data.assert_called_once_with("test")
