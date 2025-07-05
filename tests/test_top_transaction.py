from unittest.mock import patch

import pytest

from src.utils import top_transaction
from tests.conftest import return_sorted_dataframe
import pandas as pd

@pytest.mark.parametrize('exception',
                         [[
                            {'date': '01.12.2021', 'amount': -160.89, 'category': 'Супермаркеты', 'description': 'Колхоз'},
                            {'date': '01.12.2021', 'amount': -64.0, 'category': 'Супермаркеты', 'description': 'Колхоз'},
                            {'date': '02.12.2021', 'amount': -118.12, 'category': 'Такси', 'description': 'Вези меня'},
                            {'date': '02.12.2021', 'amount': -51.0, 'category': 'Такси', 'description': 'Вези меня'},
                            {'date': '04.12.2021', 'amount': -1000.0,'category': 'Супермаркеты', 'description': 'Магнит'}
                         ]])
def test_top_transaction(return_sorted_dataframe, exception):
    """Тест успешного возврата топ 5 расходов"""
    assert top_transaction(return_sorted_dataframe) == exception


def test_top_transaction_empty_df():
    """Тестирование случая когда в функцию передан пустой датафрейм"""
    assert top_transaction(pd.DataFrame([])) == []


def test_top_transaction_exception(return_sorted_dataframe):
    """Тестирование случая, когда при выполнении функции возникает ошибка"""
    with patch.object(return_sorted_dataframe,'sort_values', side_effect= KeyError) as mock_sort:
        assert top_transaction(return_sorted_dataframe) == []
        mock_sort.assert_called_once_with('Сумма платежа', ascending=False, key=abs)