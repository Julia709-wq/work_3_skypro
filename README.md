## **Веб-страницы**
### Главная

В модуле main находится главная функция приложения. Функция принимает дату в формате _YYYY-MM-DD HH:MM:SS_ и возвращает JSON-ответ
со следующими данными: 
1. Приветствие 
2. По каждой карте: последние 4 цифры номера карты, общая сумма расходов и кэшбек (в расчёте 1 рубль на каждые 100 рублей).
3. Топ 5 транзакций по сумме платежа
4. Курс валют
5. Стоимость акций из S&P500

Данные о транзакциях хранятся в файле operations.xlsx в директории data. 

Функция, генерирующая JSON-ответ находится в модуле views. Эта функция вызывает внутри себя вспомогательные функции, 
которые хранятся в модуле utils:
- read_data_from_file(): функция, читающая данные из файла operations
- get_greeting(): функция, генерирующая приветствие пользователя, в зависимости от текущего времени
- calculate_cashback(): функция, рассчитывающая кэшбек от общей суммы расходов
- get_card_info(): функция, возвращающая словарь с данными по картам
- get_top_transaction(): функция, возвращающая топ-5 транзакций по величине расхода
- get_currency_rate(): функция, возвращающая курс валют, необходимых пользователю
- get_stock_prices(): функция, возвращающая стоимости акций, необходимых пользователю

Данные для последних двух функций находятся в файле user_settings.json.

## **Сервисы**

В модуле services расположены дополнительные сервисы: 
1. simple_search() - функция простого поиска по строке-образцу
2. search_personal_transfers() - функция поиска переводов физическим лицам

## **Отчеты**

В модуле reports находится декоратор для записи результата работы функции в файл. Сама функция возвращает траты по заданной категории
за последние три месяца. Пример отчета находится в директории src.

Для всех реализованных функций в директории tests имеются тесы, проверяющие их работу. 


