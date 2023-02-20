import requests
from bs4 import BeautifulSoup

URL = 'https://bookflow.ru/it-shutki-pro-programmistov-yumor-razrabotchikov/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko)'
                         ' Version/14.0.1 Safari/605.1.15',
           'accept': '*/*'}


def parsing_of_memes(src):

    """
    данная функция получает текст HTML-документа с какого-то сайта с IT мемами (линк на него в URL) и возвращает
    словарь с результатом, где ключ - подпись к мему, а значение - url на фото мема

    :param src: текст HTML-документа
    :return: возвращает словарь с результатом
    """

    soup = BeautifulSoup(src, 'lxml')

    photo_urls = {}

    data_urls = soup.find_all('figure', class_='wp-caption alignnone')
    for item in data_urls:
        photo_urls[item.find('noscript').find_next()['alt']] = item.find('noscript').find_next()['src']

    return photo_urls


def parse_result():

    """
    данная функция парсит данные с сайта с IT мемами (линк на него в URL) и при ошибке доступа к нему сообщает о ней,
    иначе возвращает результат в виде словаря

    :return: возвращает результат в виде словаря
    """

    if req.status_code == 200:
        src = req.text
        return parsing_of_memes(src)
    return 'Sorry, an error occurred...😢 We are working on it now! 🙃'


# начало работы программы

req = requests.get(url=URL, headers=HEADERS)  # получает ответ с сайта с IT мемами для выполнения функции
result_of_meme_parsing = parse_result()  # словарь (в хорошем случае 🙂) по ключу и значению которого бот в main.py вернет нужное значение

# конец работы программы
