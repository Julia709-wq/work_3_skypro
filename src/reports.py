import pandas as pd
from datetime import datetime, timedelta
from functools import wraps
from src.utils import read_data_from_file
import logging

logger = logging.getLogger('reports')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('reports.log', mode='w')
file_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def report_decorator(filename=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            file_name = filename if filename else f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

            with open(file_name, "w", encoding="utf-8") as file:
                file.write(str(result))

            return result

        return wrapper

    return decorator


@report_decorator()
def generate_report(df, category, target_date=None):
    """Функция возвращает траты по заданной категории за последние три месяца"""

    try:
        logger.info("Checking for target_date")
        if target_date is None:
            logger.info("Setting target_date as current")
            target_date = datetime.now()

        elif isinstance(target_date, str):
            logger.info("Changing target_date's type to datetime")
            target_date = datetime.strptime(target_date, "%Y-%m-%d")

        df = df.copy()
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%Y-%m-%d")

        start_date = target_date - timedelta(days=90)

        logger.info("Filtering the DataFrame")
        filtered_df = df[(df["Категория"] == category) &
                         (df["Дата операции"] >= start_date) &
                         (df["Дата операции"] <= target_date)]

        total_spent = filtered_df["Сумма операции"].abs().sum()

        return f"Траты по категории '{category}' за последние три месяца: {total_spent} RUB"

    except Exception as ex:
        logger.error(f"An error occurred: {ex}")
        return f"Возникла ошибка: {ex}"


if __name__ == "__main__":
    data = read_data_from_file()
    df = pd.DataFrame(data)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    print(generate_report(df, "Переводы", "2019-02-19"))
