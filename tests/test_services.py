from unittest.mock import patch

from src.services import search_for_transfers


def test_search_for_transfers(return_excel_transfers, result_transfers):
    """Тестирование успешной работы функции"""
    assert search_for_transfers(return_excel_transfers) == result_transfers


def test_search_for_transfers_error(return_excel_transfers, transfers_error):
    """Тестирование случая возникновения ошибки в работе функции"""
    with patch("pandas.DataFrame", side_effect=Exception) as mock:
        assert search_for_transfers(return_excel_transfers) == transfers_error
        mock.assert_called_once_with = search_for_transfers(return_excel_transfers)
