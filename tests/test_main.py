from unittest.mock import patch
from src.main import start_functionality


def test_start_functionality(monkeypatch, result_transfers):
    """Тестирование успешной работы функции"""
    with (
        patch('src.main.get_date', return_value="2021-12-31 12:22:52"),
        patch('pandas.DataFrame'),
        patch('src.main.excel_file_reader') as mock_excel,
        patch('src.main.get_user_operations', return_value='ok.return.get_user_operations'),
        patch('src.main.search_for_transfers', return_value='ok.return.search_for_transfers'),
        patch('src.main.write_to_file'),
        patch('src.main.spending_by_category')
    ):
        mock_excel.return_value = result_transfers
        responses = iter(['31.12.2021', 'Транспорт', 'Да', 'Report'])
        monkeypatch.setattr('builtins.input', lambda _: next(responses))

        result = start_functionality()
        assert result == ('ok.return.get_user_operations', 'ok.return.search_for_transfers')
