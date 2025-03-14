import re
import os
import json
import pandas as pd


def simple_search(search_string: str, transactions: list):
    """Функция поиска транзакции по совпадениям строки поиска"""
    result = []
    for transaction in transactions:
        if (re.findall(search_string, transaction['Описание']) or
                re.findall(search_string, str(transaction['Категория']))):
            result.append(transaction)

    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return json_result


def search_personal_transfers(transactions: list):
    """Функция, возвращающая операции, являющиеся переводами физическим лицам"""
    result = []
    pattern = re.compile(r"\b[А-ЯЁ][а-яё]+\s*[А-ЯЁ]\.")

    for transaction in transactions:
        description = transaction["Описание"]
        if transaction["Категория"] == "Переводы" and re.findall(pattern, description):
            result.append(transaction)

    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return json_result


current_dir = os.path.dirname(__file__)
data_dir = os.path.join(current_dir, '..', 'data')

file_excel_path = os.path.join(data_dir, 'operations.xlsx')
file_excel_path = os.path.normpath(file_excel_path)

data = pd.read_excel(file_excel_path)
result_dict = data.to_dict('records')

# print(simple_search("Госуслуги", result_dict))

# print(search_personal_transfers(result_dict))
