import os
from unittest.mock import patch, MagicMock

from src.utils import get_exchange_currency


def test_get_exchange_currency_empty_list():
    """Тестирование случая когда список акций пуст"""
    assert  get_exchange_currency([]) == []


def test_get_exchange_currency_error_request():
    """Тестирование случая когда запрос к сервису не удался"""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {'ticker': 'EUR', "price": 100}
    url = os.getenv('URL_CURRENCY')
    apy_key = os.getenv('API_KEY_CURRENCY')
    get_params = {
        'get': 'rates',
        'pairs': 'EURRUB',
        "key": apy_key
    }
    headers = {'X-Api-Key': apy_key}
    with patch('requests.get') as mock_get:
        mock_get.return_value = mock_response
        assert get_exchange_currency(['EUR']) == []
        mock_get.assert_called_once_with(url, params=get_params)


def test_stocks_prices():
    """Тестирование успешного получения курсов валют"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
          "currency": 'EURRUB',
          "data" : {'EURRUB' : 100}
        }
    url = os.getenv('URL_CURRENCY')
    apy_key = os.getenv('API_KEY_CURRENCY')
    get_params = {
        'get': 'rates',
        'pairs': 'EURRUB',
        "key": apy_key
    }
    headers = {'X-Api-Key': apy_key}
    with patch('requests.get') as mock_get:
        mock_get.return_value = mock_response
        assert get_exchange_currency(['EUR']) == [{'currency': 'EUR', 'rate': 100}]
        mock_get.assert_called_once_with(url, params=get_params)