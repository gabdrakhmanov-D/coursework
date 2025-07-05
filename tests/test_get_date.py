from freezegun import freeze_time


import pytest

from src.utils import get_date


@pytest.mark.parametrize('date, exception', (['2006-07-05 10:34:09.044074', '2006-07-05 10:34:09'],
                                             ['2015-07-05 10:34:09.044074', '2015-07-05 10:34:09'],
                                             ['2025-07-05 10:34:09.044074', '2025-07-05 10:34:09']))
def test_get_date(exception,date):
    """Тестирование возврата текущей даты"""
    with freeze_time(date):
        assert get_date() == exception