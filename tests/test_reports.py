import pytest
import os
from datetime import datetime, timedelta
import pandas as pd
from src.reports import report_decorator, generate_report


@pytest.fixture
def transactions_data():
    date1 = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
    date2 = (datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d")
    date3 = (datetime.now() - timedelta(days=40)).strftime("%Y-%m-%d")
    date4 = (datetime.now() - timedelta(days=100)).strftime("%Y-%m-%d")
    data = pd.DataFrame([
            {"Дата операции": date1, "Сумма операции": -1000.0, "Категория": "Еда", "Описание": "Магазин"},
            {"Дата операции": date2, "Сумма операции": -1500.0, "Категория": "Переводы", "Описание": "Иван Ф."},
            {"Дата операции": date3, "Сумма операции": -2000.0, "Категория": "Переводы", "Описание": "Ольга С."},
            {"Дата операции": date4, "Сумма операции": -3000.0, "Категория": "Одежда", "Описание": "Магазин"},
        ])
    return data

@pytest.fixture
def test_date():
    test_date = datetime.now().strftime("%Y-%m-%d")
    return test_date

def test_generate_report(transactions_data, test_date):
    result = generate_report(transactions_data, "Еда", test_date)
    assert result == "Траты по категории 'Еда' за последние три месяца: 1000.0 RUB"

def test_generate_report_with_nonexistent_category(transactions_data, test_date):
    result = generate_report(transactions_data, "Нет такой категории", test_date)
    assert result == "Траты по категории 'Нет такой категории' за последние три месяца: 0.0 RUB"

def test_report_decorator_file_created(transactions_data):
    test_filename = "test_reports.txt"

    decorated_func = report_decorator(filename=test_filename)(generate_report)
    decorated_func(transactions_data, "Еда")
    assert os.path.exists(test_filename)

    with open(test_filename, 'r', encoding='utf-8') as f:
        content = f.read()
        assert content == "Траты по категории 'Еда' за последние три месяца: 1000.0 RUB"

    os.remove(test_filename)