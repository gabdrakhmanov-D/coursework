import os
from unittest.mock import MagicMock, patch

from src.utils import get_stocks_prices


def test_stocks_prices_error_request():
    """Тестирование случая когда запрос к сервису не удался"""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"ticker": "AMZN", "price": 100}
    url = os.getenv("URL_STOCK")
    apy_key = os.getenv("API_KEY_STOCK")
    params = {"ticker": "AMZN"}
    headers = {"X-Api-Key": apy_key}
    with patch("requests.get") as mock_get:
        mock_get.return_value = mock_response
        assert get_stocks_prices(["AMZN"]) == ["Данные не получены"]
        mock_get.assert_called_once_with(url, headers=headers, params=params)


def test_stocks_prices():
    """Тестирование успешного получения курсов валют"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"ticker": "AMZN", "price": 100}
    url = os.getenv("URL_STOCK")
    apy_key = os.getenv("API_KEY_STOCK")
    params = {"ticker": "AMZN"}
    headers = {"X-Api-Key": apy_key}
    with patch("requests.get") as mock_get:
        mock_get.return_value = mock_response
        assert get_stocks_prices(["AMZN"]) == [{"stock": "AMZN", "price": 100}]
        mock_get.assert_called_once_with(url, headers=headers, params=params)
