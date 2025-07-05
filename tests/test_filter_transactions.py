from unittest.mock import patch
import pandas as pd
import pytest

from src.utils import filter_transactions
from tests.conftest import return_excel


@pytest.mark.parametrize('date, exception',
                           [
                             (
                              '2021-12-03 00:00:00',
                               {
                                'Дата операции': ['01.12.2021 16:44:00', '02.12.2021 16:42:04', '03.12.2021 16:39:04'],
                                'Дата платежа': ['01.12.2021', '02.12.2021','03.12.2021'],
                                'Номер карты': ['*7197', '*7197', '*7197'],
                                'Сумма операции': [-160.89, -64.0, -118.12],
                                'Сумма платежа': [-160.89, -64.0, -118.12],
                                'Категория': ['Супермаркеты', 'Супермаркеты', 'Супермаркеты'],
                                'Описание': ['Колхоз', 'Колхоз', 'Магнит'],
                                }
                             )
                           ]
                        )
def test_filter_transactions(return_excel, date, exception):
    """Тестирование успешной фильтрации транзакций"""
    test_df = pd.DataFrame(exception)
    test_df['Дата операции'] = pd.to_datetime(test_df['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    assert  filter_transactions(return_excel, date).to_dict() == test_df.to_dict()


def test_empty_list_transact():
    """Тестирование получения пустого списка транзакций"""
    assert filter_transactions([], '2021-12-04 16:39:04').empty