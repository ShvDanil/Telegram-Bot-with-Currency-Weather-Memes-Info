import requests
from bs4 import BeautifulSoup

URL = 'https://cbr.ru/currency_base/daily/'
HEADERS = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15'
}


def parsing_of_currency(src):
    """
    функция парсинга данных: принимает на вход текст HTML-документа, работает с ним и возвращает вложенный
    лист, состоящий из заголовков таблицы с сайта и данных валют парсинга

    :param src: текст HTML-документа
    :return: вложенный лист, состоящий из заголовков таблицы с сайта и данных валют парсинга
    """

    soup = BeautifulSoup(src, 'lxml')
    nested_list_with_currency_data = []

    currency_data = soup.find(class_='table').find(class_='data').find('tbody').find_all('tr')
    for item in currency_data:
        item_elements = item.text.strip().split('\n')
        nested_list_with_currency_data.append(item_elements)

    return nested_list_with_currency_data


def get_final_content(lst):
    """
    создает словарь состоящий из ключа - кнопка для выбора валюты, интересующей пользователя, и значения - текущие
    данные с сайта ЦБ РФ, раздела daily данных валюты

    :param lst: принимает вложенный лист, состоящий из заголовков таблицы с сайта и данных валют парсинга
    :return: возвращает словарь для удобного вывода данных, которые запросил пользователь и отправки их боту
    """

    currency_buttons = {}
    for list_with_data in lst[1:]:
        currency_buttons[
            list_with_data[-3] + ' ' + list_with_data[-2] + ' 🏧'] = f'{list_with_data[2]} {list_with_data[1]} ' \
                                                                     f'= {list_with_data[-1]} ₽'
    return currency_buttons


def parse_result():
    """
    данная функция парсит данные с сайта ЦБ РФ раздела daily данных валют и при ошибке доступа к нему сообщает о ней,
    иначе возвращает результат в виде словаря

    :return: возвращает результат в виде словаря или сообщает о возникшей ошибке
    """

    if req.status_code == 200:
        src = req.text
        list_with_currency_data = parsing_of_currency(src)
        return get_final_content(list_with_currency_data)
    return 'Sorry, an error occurred...😢 We are working on it now! 🙃'


# начало работы программы

req = requests.get(url=URL, headers=HEADERS)  # получает ответ с сайта ЦБ РФ для выполнения функции
result_of_currency_parsing = parse_result()  # словарь (в хорошем случае 🙂) по ключу которого бот в main.py вернет нужное значение

# конец работы программы
