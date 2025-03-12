import datetime


def gen_greeting():
    current_time = datetime.datetime.now()
    if datetime.time(5, 0, 0) <= current_time.time() <= datetime.time(12, 0, 0):
        return "Доброе утро!"
    elif datetime.time(12, 0, 1) <= current_time.time() <= datetime.time(16, 59,59):
        return "Добрый день!"
    elif datetime.time(17, 0, 0) <= current_time.time() <= datetime.time(23, 59,59):
        return "Добрый вечер!"
    elif datetime.time(0, 0, 0) <= current_time.time() <= datetime.time(5, 59,59):
        return "Доброй ночи!"





