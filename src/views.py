import datetime
import json
from src.utils import (get_greeting, get_card_info, get_top_transactions,
                       get_stock_prices, get_currency_rate)



def generate_json_response(date_time_str, transactions):
    """Функция генерации JSON-ответа"""
    date_time = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    greeting = get_greeting()

    cards = {}
    for transaction in transactions:

        card_number = str(transaction['Номер карты']).replace(".", "").replace("*", "")
        card_last_digits = card_number[-4:]
        if card_last_digits not in cards:
            cards[card_last_digits] = []
        cards[card_last_digits].append(transaction)

    card_info_list = [get_card_info(transactions) for transactions in cards.values()]

    top_transactions = get_top_transactions(transactions)

    with open("user_settings.json", "r", encoding="utf-8") as f:
        user_settings = json.load(f)

    currency_rates = get_currency_rate(user_settings.get("user_currencies", []))

    stock_prices = get_stock_prices(user_settings.get("user_stocks", []))

    response = {
        "greeting": greeting,
        "cards": card_info_list,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    return response


