import datetime


def get_date():
    """Функция, которая возвращает строку с датой и временем в формате YYYY-MM-DD HH:MM:SS."""
    current_date_time = datetime.datetime.now()
    date_str= current_date_time.strftime("%Y-%m-%d %H:%M:%S")
    return date_str

