import re
import json
import logging


logger = logging.getLogger('services')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('services.log', mode='w')
file_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def simple_search(search_string: str, transactions: list):
    """Функция поиска транзакции по совпадениям строки поиска"""
    try:
        result = []
        logger.info("The search started")
        for transaction in transactions:
            if (re.findall(search_string, transaction['Описание']) or
                    re.findall(search_string, str(transaction['Категория']))):
                result.append(transaction)

        logger.info("The search is finished")
        json_result = json.dumps(result, ensure_ascii=False, indent=4)
        return json_result

    except Exception as ex:
        logger.error(f'An error occurred: {ex}')


def search_personal_transfers(transactions: list):
    """Функция, возвращающая операции, являющиеся переводами физическим лицам"""
    try:
        logger.info("The search for transfers started")
        result = []
        pattern = re.compile(r"\b[А-ЯЁ][а-яё]+\s*[А-ЯЁ]\.")

        for transaction in transactions:
            description = transaction["Описание"]
            if transaction["Категория"] == "Переводы" and re.findall(pattern, description):
                result.append(transaction)

        logger.info("The search for transfers is finished")
        json_result = json.dumps(result, ensure_ascii=False, indent=4)
        return json_result

    except Exception as ex:
        logger.error(f'An error occurred: {ex}')