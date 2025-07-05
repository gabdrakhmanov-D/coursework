from unittest.mock import patch

import pytest
import pandas as pd

from src.utils import excel_file_reader


@pytest.mark.parametrize(
    "expected",
    [
        [
            {
                "id": 650703,
                "state": "EXECUTED",
                "date": "2023-09-05T11:30:32Z",
                "amount": 16210,
                "currency_name": "Sol",
                "currency_code": "PEN",
                "from": "Счет 58803664561298323391",
                "to": "Счет 39745660563456619397",
                "description": "Перевод организации",
            }
        ]
    ],
)
@patch("pandas.read_excel")
def test_excel_file_reader(df_mock, expected):
    """Тестирование успешного чтения Excel файла"""
    mock_data = pd.DataFrame(
        {
            "id": [650703],
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210,
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        }
    )
    df_mock.return_value = mock_data
    assert excel_file_reader("path") == expected
    df_mock.assert_called_once_with("path")


def test_excel_file_reader_no_file():
    """Тестирование случая когда Excel файл не найден"""
    with patch("pandas.read_excel", side_effect=FileNotFoundError) as df_mock:
        assert excel_file_reader("path") == []
        df_mock.assert_called_once_with("path")


def test_excel_file_reader_str():
    """Тестирование случая когда Excel файл пустой"""
    with patch("pandas.read_excel") as df_mock:
        mock_data = pd.DataFrame([])
        df_mock.return_value = mock_data
        assert excel_file_reader("path") == []
        df_mock.assert_called_once_with("path")
