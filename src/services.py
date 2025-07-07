import json
import logging
import re

import pandas as pd

logger_transfers = logging.Logger('search_for_transfers')


def search_for_transfers(list_transactions: list) -> json:
    """Функция возвращает JSON со всеми транзакциями, которые относятся к переводам физлицам."""
    logger_transfers.info('Старт работы функции')
    try:
        df_transactions = pd.DataFrame(list_transactions)
        result_df = df_transactions[df_transactions["Категория"] == 'Переводы']
        logger_transfers.info('Выполнена фильтрация по категории "Переводы"')
        transfers_df = result_df[result_df["Описание"].str.match(r'^\w+ \b\w\.', case=False, flags=re.IGNORECASE)]
        logger_transfers.info('Выполнена фильтрация по паттерну')
        dict_transfers = transfers_df.to_dict('records')
        result_json = json.dumps(dict_transfers, ensure_ascii= False, indent=4)
        logger_transfers.info('Успешная конвертация в JSON и возврат результата')
        return result_json
    except Exception as ex:
        logger_transfers.error(f'Ошибка в работе функции: {ex}')
        return json.dumps('Не удалось получить список переводов', ensure_ascii= False)
