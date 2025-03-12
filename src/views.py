import datetime
import requests


def get_greeting(time):
    """Функция приветствия"""
    hour = time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def calculate_cashback(total_spent):
    """Функция подсчета кэшбека"""
    return total_spent // 100


def get_card_info(card_transactions):
    """Функция вывода данных по картам"""
    card_number = str(card_transactions[-1]['Номер карты']).replace(".", "").replace("*", "")
    total_spent = abs(sum(t['Сумма операции'] for t in card_transactions if t['Сумма операции'] < 0))
    cashback = calculate_cashback(total_spent)

    card_info = {
        "last_digits": card_number[-4:],
        "total_spent": total_spent,
        "cashback": cashback
    }
    return card_info


def get_top_transactions(transactions, top_n=5):
    """Функция сортировки транзакций"""
    expenses = [t for t in transactions if t['Сумма операции'] < 0]
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


def get_currency_rate():
    pass


def generate_json_response(date_time_str, transactions):
    """Функция генерации JSON-ответа"""
    date_time = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    greeting = get_greeting(date_time)

    cards = {}
    for transaction in transactions:

        card_number = str(transaction['Номер карты']).replace(".", "").replace("*", "")
        card_last_digits = card_number[-4:]
        if card_last_digits not in cards:
            cards[card_last_digits] = []
        cards[card_last_digits].append(transaction)

    card_info_list = [get_card_info(transactions) for transactions in cards.values()]

    top_transactions = get_top_transactions(transactions)

    response = {
        "greeting": greeting,
        "cards": card_info_list,
        "top_transactions": top_transactions
    }

    return response


# "currency_rates": [
#     {
#       "currency": "USD",
#       "rate": 73.21
#     },
#     {
#       "currency": "EUR",
#       "rate": 87.08
#     }
#   ],
#   "stock_prices": [
#     {
#       "stock": "AAPL",
#       "price": 150.12
#     },
#     {
#       "stock": "AMZN",
#       "price": 3173.18
#     },
#     {
#       "stock": "GOOGL",
#       "price": 2742.39
#     },
#     {
#       "stock": "MSFT",
#       "price": 296.71
#     },
#     {
#       "stock": "TSLA",
#       "price": 1007.08
#     }
#   ]
