import requests
import pandas as pd
from datetime import datetime
import os
import logging


logger = logging.getLogger('utils')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('utils.log', mode='w')
file_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_data_from_file():
    """Функция чтения данных из файла"""
    try:
        logger.info("Reading data from file")

        current_dir = os.path.dirname(__file__)
        data_dir = os.path.join(current_dir, '..', 'data')

        file_excel_path = os.path.join(data_dir, 'operations.xlsx')
        file_excel_path = os.path.normpath(file_excel_path)

        data = pd.read_excel(file_excel_path)
        result_dict = data.to_dict('records')

        return result_dict

    except Exception as ex:
        logger.error(f'An error occurred: {ex}')


def get_greeting():
    """Функция приветствия, зависящая от текущего времени"""
    try:
        logger.info("Greeting the user")
        hour = datetime.now().hour  # Получаем текущий час
        if 5 <= hour < 12:
            return "Доброе утро"
        elif 12 <= hour < 18:
            return "Добрый день"
        elif 18 <= hour < 22:
            return "Добрый вечер"
        else:
            return "Доброй ночи"

    except Exception as ex:
        logger.error(f'An error occurred: {ex}')


def calculate_cashback(total_spent):
    """Функция подсчета кэшбека"""
    return total_spent // 100


def get_card_info(card_transactions):
    """Функция вывода данных по картам"""
    try:
        logger.info("Getting information about user's cards")
        card_number = str(card_transactions[-1]['Номер карты']).replace(".", "").replace("*", "")
        total_spent = abs(sum(t['Сумма операции'] for t in card_transactions if t['Сумма операции'] < 0))
        cashback = calculate_cashback(total_spent)

        card_info = {
            "last_digits": card_number[-4:],
            "total_spent": total_spent,
            "cashback": cashback
        }
        return card_info

    except Exception as ex:
        logger.error(f'An error occurred: {ex}')


def get_top_transactions(transactions, top_n=5):
    """Функция сортировки транзакций"""
    try:
        logger.info("Counting total expenses")
        expenses = [t for t in transactions if t['Сумма операции'] < 0]
        logger.info("Sorting transactions")
        sorted_transactions = sorted(expenses, key=lambda x: abs(x['Сумма операции']), reverse=True)
        top_transactions = []

        for t in sorted_transactions[:top_n]:
            top_transactions.append({
                "date": t['Дата операции'],
                "amount": abs(t['Сумма операции']),
                "category": t['Категория'],
                "description": t['Описание']
            })
        return top_transactions

    except Exception as ex:
        logger.error(f'An error occurred: {ex}')


def get_currency_rate(currencies):
    """Функция, которая обращается к API и возвращает курс валют"""
    try:
        API_KEY = "06677ff6ea795c05f663f1a0"
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/RUB"

        try:
            logger.info("Requesting information on currency rates from API-server")
            response = requests.get(url)
            response.raise_for_status()
            logger.info("Getting response from API-server")
            data = response.json()

            rates = data.get("conversion_rates", {})

            currency_rates = []

            for currency in currencies:
                rate = rates.get(currency)
                if rate:
                    inverted_rate = 1 / rate
                    currency_rates.append({"currency": currency, "rate": round(inverted_rate, 4)})
            return currency_rates
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении курсов валют: {e}")
            return []

    except Exception as ex:
        logger.error(f'An error occurred: {ex}')


def get_stock_prices(stocks):
    """Функция, которая обращается к API и возвращает стоимость акций"""
    try:
        api_KEY = "F745P91K8IVFUY6S"
        stock_prices = []

        for stock in stocks:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_KEY}"
            try:
                logger.info("Requesting information on stocks rates from API-server")
                response = requests.get(url)
                response.raise_for_status()
                logger.info("Getting response from API-server")
                data = response.json()

                price = float(data.get("Global Quote", {}).get("05. price", 0))
                stock_prices.append({"stock": stock, "price": price})
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при получении данных о акции {stock}: {e}")

        return stock_prices

    except Exception as ex:
        logger.error(f'An error occurred: {ex}')
