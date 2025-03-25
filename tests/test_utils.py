from unittest.mock import patch, Mock
import pandas as pd
import pytest
from datetime import datetime
from src.utils import (read_data_from_file, get_greeting, get_card_info,
                       get_top_transactions, get_currency_rate, get_stock_prices)


@patch('pandas.read_excel')
def test_read_data_from_file(mock_read_excel):
    mock_excel_data = pd.DataFrame([{
        'Дата операции': '01.01.2018 12:49:53',
        'Дата платежа': '01.01.2018',
        'Статус': 'OK',
        'Сумма операции': -3000.0,
        'Валюта операции': 'RUB'
    }])

    mock_read_excel.return_value = mock_excel_data

    result = read_data_from_file()

    expected_result = [{
        'Дата операции': '01.01.2018 12:49:53',
        'Дата платежа': '01.01.2018',
        'Статус': 'OK',
        'Сумма операции': -3000.0,
        'Валюта операции': 'RUB'
    }]

    assert result == expected_result
    mock_read_excel.assert_called_once()


@patch('src.utils.datetime')
def test_get_greeting_morning(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 10, 15, 8, 0, 0)
    result = get_greeting()
    assert result == "Доброе утро"

@patch('src.utils.datetime')
def test_get_greeting_afternoon(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 10, 15, 14, 0, 0)
    result = get_greeting()
    assert result == "Добрый день"

@patch('src.utils.datetime')
def test_get_greeting_evening(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 10, 15, 20, 0, 0)
    result = get_greeting()
    assert result == "Добрый вечер"

@patch('src.utils.datetime')
def test_get_greeting_night(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 10, 15, 3, 0, 0)
    result = get_greeting()
    assert result == "Доброй ночи"


def test_get_card_info():
    transactions = [{"Номер карты": "1234.5678.9012.3456", "Сумма операции": -1000.0},
                    {"Номер карты": "1234.5678.9012.3456", "Сумма операции": -500.0},
                    {"Номер карты": "1234.5678.9012.3456", "Сумма операции": -300.0}]

    result = get_card_info(transactions)
    expected_result = {
            "last_digits": '3456',
            "total_spent": 1800,
            "cashback": 18
        }
    assert result == expected_result


def test_get_card_info_empty_transactions():
    transactions = []
    assert get_card_info(transactions) == None


def test_get_top_transactions():
    transactions = [
        {"Дата операции": "2023-10-01", "Сумма операции": -1000.0, "Категория": "Еда", "Описание": "Магазин"},
        {"Дата операции": "2023-10-02", "Сумма операции": -500.0, "Категория": "Транспорт", "Описание": "Такси"},
        {"Дата операции": "2023-10-03", "Сумма операции": -1500.0, "Категория": "Развлечения", "Описание": "Кино"},
        {"Дата операции": "2023-10-04", "Сумма операции": -200.0, "Категория": "Еда", "Описание": "Кафе"},
        {"Дата операции": "2023-10-05", "Сумма операции": -3000.0, "Категория": "Одежда", "Описание": "Магазин"}
    ]

    expected_result = [
        {"date": "2023-10-05", "amount": 3000.0, "category": "Одежда", "description": "Магазин"},
        {"date": "2023-10-03", "amount": 1500.0, "category": "Развлечения", "description": "Кино"},
        {"date": "2023-10-01", "amount": 1000.0, "category": "Еда", "description": "Магазин"},
    ]

    result = get_top_transactions(transactions, top_n=3)
    assert result == expected_result

def test_get_top_transactions_empty_list():
    transactions = []
    assert get_top_transactions(transactions) == []

@patch('requests.get')
def test_get_currency_rate(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "conversion_rates": {
            "USD": 0.014,
            "EUR": 0.012,
        }
    }
    mock_get.return_value = mock_response
    currencies = ["USD", "EUR"]
    expected_result = [
        {"currency": "USD", "rate": round(1 / 0.014, 4)},  # 1 USD = 71.4286 RUB
        {"currency": "EUR", "rate": round(1 / 0.012, 4)},  # 1 EUR = 83.3333 RUB
    ]

    result = get_currency_rate(currencies)
    assert result == expected_result
    mock_get.assert_called_once()


@patch('requests.get')
def test_get_stock_prices(mock_get):
    mock_response_google = Mock()
    mock_response_google.status_code = 200
    mock_response_google.json.return_value = {
            "Global Quote": {
                "05. price": "2800.75",
            }
        }

    mock_response_apple = Mock()
    mock_response_apple.status_code = 200
    mock_response_apple.json.return_value = {
        "Global Quote": {
            "05. price": "150.50",
        }
    }

    mock_get.side_effect = [mock_response_apple, mock_response_google]
    stocks = ["AAPL", "GOOGL"]
    expected_result = [
        {"stock": "AAPL", "price": 150.50},
        {"stock": "GOOGL", "price": 2800.75},
    ]

    result = get_stock_prices(stocks)
    assert result == expected_result
