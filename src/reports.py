import datetime
import json
import logging
from datetime import datetime
from typing import Optional, Callable, Any
from dateutil.relativedelta import relativedelta
import pandas as pd
from functools import wraps

from config import PATH_TO_OPERATIONS
from src.utils import excel_file_reader, get_date

data = excel_file_reader(PATH_TO_OPERATIONS)
df = pd.DataFrame(data)
logger_write_to_file = logging.Logger('write_to_file')


def write_to_file(filename: str = None):
    """Декоратор, который записывает отчет в файл. Если передано имя файла создает файл с этим именем,
     иначе файл называется report_by_category.json"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            argument_func, kw_argument_func = args, kwargs
            function_name = func.__name__
            result = func(*args, **kwargs)
            if filename:
                with open(f'{filename}.json', 'w', encoding ='utf-8',) as file:
                    json.dump(result, file, ensure_ascii=False, indent=4)
                return result
            else:
                with open(f'report_by_category.json', 'w', encoding ='utf-8',) as file:
                    json.dump(result, file, ensure_ascii=False, indent=4)
                return result
        return wrapper
    return decorator


@write_to_file()
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         current_date: Optional[str] = None) -> pd.DataFrame:
    if not current_date:
        current_date = datetime.today()
    else:
        current_date = datetime.strptime(current_date, "%d.%m.%Y").date()
    start_date = current_date - relativedelta(months=3)
    end_date = current_date + relativedelta(days=1)

    end_date = end_date.strftime("%Y-%m-%d")
    start_date = start_date.strftime("%Y-%m-%d")
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    filtered_df = transactions[(transactions['Дата операции'] >= start_date) & (df['Дата операции'] <= end_date)]
    category_df = filtered_df[filtered_df['Категория'] == category]
    category_df["Дата операции"] = category_df["Дата операции"].apply(lambda x: x.strftime("%d.%m.%Y"))

    return category_df.to_dict('records')

f = spending_by_category(df,'Ж/д билеты', '31.12.2021')


print(f)
