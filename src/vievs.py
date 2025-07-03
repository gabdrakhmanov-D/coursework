import logging

from src.utils import get_date

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s',
                    filename='C:/Users/rubik/OneDrive/Documents/Pyton/course_work/logs/application.log',
                    filemode='w',
                    encoding='utf-8')

logger_file = logging.getLogger('select_file')
logger_filter = logging.getLogger('select_filter')
logger_sort_by_data = logging.getLogger('sort_by_data')
logger_rub_transact = logging.getLogger('rub_transact')
logger_by_pattern = logging.getLogger('filter_by_pattern')
logger_main = logging.getLogger('main')

def main():
    current_date = get_date()
    if 12 > int(current_date[11:13]) > 6:
        greeting_value = 'Доброе утро!'
    elif 18 > int(current_date[11:13]) > 12:
        greeting_value = 'Добрый день!'
    elif 24 > int(current_date[11:13]) > 18:
        greeting_value = 'Добрый вечер!'
    else:
        greeting_value = 'Доброй ночи'
    return greeting_value
if __name__ == '__main__':
    print(main())
