from unittest.mock import patch, Mock

import pytest

from src.utils import get_date


@pytest.mark.parametrize('date, exception', (['2006-07-05 10:34:09.044074', '2006-07-05 10:34:09'],
                                             ['2015-07-05 10:34:09.044074', '2015-07-05 10:34:09'],
                                             ['2025-07-05 10:34:09.044074', '2025-07-05 10:34:09']))
def test_get_date(date,exception):
    """Тестирование возврата текущей даты"""
    pass