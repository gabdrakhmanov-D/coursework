import json
import logging
from datetime import datetime
from functools import wraps

import pandas as pd
from dateutil.relativedelta import relativedelta

logger_write_to_file = logging.Logger('write_to_file')
logger_spending = logging.Logger('spending_by_category')


def write_to_file(filename: str = None):
    """Декоратор, который записывает отчет в файл. Если передано имя файла создает файл с этим именем,
     иначе файл называется report_by_category.json"""
    logger_write_to_file.info('Старт работы декоратора')

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if result.empty:
                logger_write_to_file.error('Поступил пустой датафрейм.')
                return result
            if filename:
                with open(f'{filename}.json', 'w', encoding='utf-8',) as file:
                    result = result.to_dict('records')
                    json.dump(result, file, ensure_ascii=False, indent=4)
                    logger_write_to_file.info(f'Запись результата в файл: {filename}')
                return result
            else:
                with open('report_by_category.json', 'w', encoding='utf-8') as file:
                    result = result.to_dict('records')
                    json.dump(result, file, ensure_ascii=False, indent=4)
                    logger_write_to_file.info('Запись результата в файл: report_by_category.json')
                return result
        return wrapper
    return decorator


@write_to_file()
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         current_date: str = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).
     Если дата не передана, то берется текущая дата. Формат даты для передачи: dd.mm.yyyy"""

    logger_spending.info('Старт работы функции')
    try:
        if not current_date:
            current_date = datetime.today()
            logger_spending.info('Дата не введена, формирование текущей даты')
        else:
            logger_spending.info('Перевод введенной даты в datetime')
            current_date = datetime.strptime(current_date, "%d.%m.%Y").date()
        start_date = current_date - relativedelta(months=3)
        end_date = current_date + relativedelta(days=1)  # Для правильной фильтрации по дате требуется прибавить 1 день

        end_date = end_date.strftime("%Y-%m-%d")
        start_date = start_date.strftime("%Y-%m-%d")
        logger_spending.info('Фильтрация датафрейма')

        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        filtered_df = transactions[(transactions['Дата операции'] >= start_date)
                                   & (transactions['Дата операции'] <= end_date)]
        category_df = filtered_df[filtered_df['Категория'] == category]
        category_df["Дата операции"] = category_df["Дата операции"].apply(lambda x: x.strftime("%d.%m.%Y"))

        logger_spending.info("Успешная фильтрация датайфрейма и его возврат")
        return category_df
    except Exception as ex:
        logger_spending.error(f'Ошибка в работе функции: {ex}')
        return pd.DataFrame()
