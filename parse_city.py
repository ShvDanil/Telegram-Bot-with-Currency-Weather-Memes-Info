import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

cities_eng = {'Москва 🇷🇺': 'Moscow', 'Париж 🇫🇷': 'Paris', 'Лондон 🇬🇧': 'London', 'Нью-Йорк 🇺🇸': 'New-york',
              'Рим 🇮🇹': 'Rome', 'Пекин 🇨🇳': 'Beijing'}

URL = 'https://time.is/'
HEADERS = {
    'Accept': '*/*',
    'User-Agent': f'{UserAgent().random}'
}


def parsing_of_weather(src):

    """
    данная функция принимает текст HTML-документа сайта и возвращает кортеж, состоящий из четырех элементов
     (1 - погодные условия в городе, 2 - температура, 3 - температура по ощущениям, 4 - местное время в городе)

    :param src: текст HTML-документа
    :return: возвращает кортеж, состоящий из четырех элементов
    """

    soup = BeautifulSoup(src, 'lxml')

    # weather_condition = soup.find(class_='fact__temp-wrap')
    # actual_tmp = soup.find(class_='temp fact__temp fact__temp_size_s').find(class_='temp__value temp__value_with-unit').text
    # feels_like_tmp = soup.find(class_='link__feelings fact__feelings').find(class_='term__value').text
    fact_time = soup.find('div', class_='w1').find('time').text[:-3]

    return fact_time


def parse_result():

    """
    данная функция парсит данные с сайта Яндекс.Погода раздела города и при ошибке доступа к нему сообщает о ней,
    иначе возвращает результат в виде кортежа из четырех элементов

    :return: возвращает результат в виде кортежа из четырех элементов
    """

    if req.status_code == 200:
        src = req.text
        return parsing_of_weather(src)
    return 'Sorry, an error occurred...😢 We are working on it now! 🙃'


# начало работы программы

result_of_city_parsing = {}  # словарь (в хорошем случае 🙂), ключом которого является город, а значением
# - кортеж из четырех элементов (подробнее о них смотреть в описании функции "parsing_of_weather"), по
# ключу которого бот в main.py вернет нужное значение


for key, value in cities_eng.items():
    req = requests.get(url=URL + value, headers=HEADERS)
    # req.encoding = 'utf-8'
    result = parse_result()
    result_of_city_parsing[key] = result
req = requests.get(url=URL, headers=HEADERS)
# req.encoding = 'utf-8'
# print(result_of_city_parsing)
# конец работы программы
# print(result_of_city_parsing)
