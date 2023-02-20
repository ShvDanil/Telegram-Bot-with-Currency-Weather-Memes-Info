import telebot
import requests
from telebot import types
from token_file import TOKEN
from random import randint, choice
from PIL import Image

bot = telebot.TeleBot(TOKEN)


# блок с кнопками основного меню

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    main_menu_buttons = ['🔸 Рандомное число 🔸', '💸 Курсы валют 💸', 'Города 🏙', 'Мем 😀', 'Смайл 🤗',
                         'Что в коробке? 📦', 'Стикер 😉', 'ℹ Информация ℹ']
    for button in main_menu_buttons:
        markup.add(types.KeyboardButton(button))

    bot.send_message(message.chat.id, 'Здравствуйте, <i>{0.first_name}</i>! 🙂✨ Рад Вас видеть!\n\n'
                                      'Для продолжения работы бота и получения интересующей Вас информации '
                                      'выберите любую из предложенных ниже кнопок\n\n'
                                      'P.S. Для начала рекомендую перейти в раздел <i>ℹ <u>Информация</u> ℹ</i>, '
                                      'который расскажет о функциях <u><i>бота</i></u> 🤖 и его '
                                      '<u><i>разработчике</i></u> 👨🏼‍💻'.format(message.from_user),
                     reply_markup=markup, parse_mode='HTML')


# конец блока с кнопками основного меню


@bot.message_handler(content_types=['text'])
def bot_message(message):
    from parse_currency import result_of_currency_parsing
    cities = ['Москва 🇷🇺', 'Париж 🇫🇷', 'Лондон 🇬🇧', 'Нью-Йорк 🇺🇸', 'Рим 🇮🇹', 'Пекин 🇨🇳']
    back_button = 'Назад 🔙'

    if message.chat.type == 'private':

        message_from_user = message.text

        # начало блока подменю кнопок основного меню

        # блок отправки пользователю рандомного числа

        if message_from_user == '🔸 Рандомное число 🔸':
            bot.send_message(message.chat.id, 'Ваше число: ' + str(randint(0, 1000)))

        # конец блока отправки пользователю рандомного числа
        # блок отправки пользователю текущего состояния курса валют

        elif message_from_user == '💸 Курсы валют 💸':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            if result_of_currency_parsing == 'Sorry, an error occurred...😢 We are working on it now! 🙃':
                bot.send_message(message.chat.id, result_of_currency_parsing)
            else:

                for button in result_of_currency_parsing.keys():
                    markup.add(types.KeyboardButton(button))
                markup.add(types.KeyboardButton(back_button))

                bot.send_message(message.chat.id, '{0.first_name}, выберите интересующую Вас валюту'.format(
                    message.from_user), reply_markup=markup)

        elif message_from_user in result_of_currency_parsing:
            bot.send_message(message.chat.id, f'На данный момент по курсу <u><a href="https://cbr.ru">ЦБ РФ</a></u>:\n'
                                              f'{result_of_currency_parsing[message_from_user]}', parse_mode='HTML')

        # конец блока отправки пользователю текущего состояния курса валют
        # блок отправки пользователю фото города и текущей погоды в нем

        elif message_from_user == 'Города 🏙':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            markup.add(
                types.KeyboardButton(cities[0]),
                types.KeyboardButton(cities[1]),
                types.KeyboardButton(cities[2]),
                types.KeyboardButton(cities[3]),
                types.KeyboardButton(cities[4]),
                types.KeyboardButton(cities[5]),
            )
            markup.add(types.KeyboardButton(back_button))

            bot.send_message(message.chat.id, 'Выберите город, чтобы узнать время в нем и взглянуть на него 🙃',
                             reply_markup=markup)

        elif message_from_user in cities:
            from parse_city import result_of_city_parsing

            if list(result_of_city_parsing.values())[0] == 'Sorry, an error occurred...😢 We are working on it now! 🙃':
                bot.send_message(message.chat.id, list(result_of_city_parsing.values())[0])
            else:
                hour_time_smile = {0: '🕛', 1: '🕐', 2: '🕑', 3: '🕒', 4: '🕓', 5: '🕔', 6: '🕕', 7: '🕖', 8: '🕗', 9: '🕘', 10: '🕙',
                                   11: '🕚', 12: '🕛', 13: '🕐', 14: '🕑', 15: '🕒', 16: '🕓', 17: '🕔', 18: '🕕', 19: '🕖',
                                   20: '🕗', 21: '🕘', 22: '🕙', 23: '🕚'}
                countries = {'Москва 🇷🇺': 'в России', 'Париж 🇫🇷': 'во Франции', 'Лондон 🇬🇧': 'в Великобритании',
                             'Нью-Йорк 🇺🇸': 'в США', 'Рим 🇮🇹': 'в Италии', 'Пекин 🇨🇳': 'в Китае'}
                local_time_hour = int(result_of_city_parsing[message_from_user][:2])

                # bot.send_message(message.chat.id,
                #                  f'Город <b>{message_from_user[:-3]}</b> расположен {countries[message_from_user]}\n'
                #                  f'Сейчас в нем {result_of_weather_parsing[message_from_user][0].lower()},'
                #                  f' температура воздуха составляет '
                #                  f'<b><i>{result_of_weather_parsing[message_from_user][1]}°</i></b>\n'
                #                  f'Ощущается как <b><i>{result_of_weather_parsing[message_from_user][2]}°</i></b>\n'
                #                  f'Местное время: <b><i>{result_of_weather_parsing[message_from_user][3]}</i></b> '
                #                  f'{hour_time_smile[local_time_hour]}',
                #                  parse_mode='HTML')

                bot.send_message(message.chat.id, f'Город <b>{message_from_user[:-3]}</b> расположен {countries[message_from_user]}\n'
                                 f'Местное время: <b><i>{result_of_city_parsing[message_from_user]}</i></b> '
                                 f'{hour_time_smile[local_time_hour]}',
                                 parse_mode='HTML')

                if 0 <= local_time_hour <= 5:
                    day_time = 'night'
                elif 6 <= local_time_hour <= 11:
                    day_time = 'morning'
                elif 12 <= local_time_hour <= 17:
                    day_time = 'day'
                else:
                    day_time = 'evening'
                with open(f'photos/cities/{day_time}/{message_from_user[:-3]}.jpg', 'rb') as city_photo:
                    bot.send_photo(message.chat.id, city_photo)

        # конец блока отправки пользователю фото города и текущей погоды в нем
        # начало блока отправки пользователю рандомного мема

        elif message_from_user == 'Мем 😀':
            from parse_meme import result_of_meme_parsing

            if result_of_meme_parsing == 'Sorry, an error occurred...😢 We are working on it now! 🙃':
                bot.send_message(message.hat.id, result_of_meme_parsing)
            else:
                meme_text = choice(list(result_of_meme_parsing.keys()))
                bot.send_message(message.chat.id, meme_text)

                meme_img = Image.open(requests.get(url=result_of_meme_parsing[meme_text], stream=True).raw)
                bot.send_photo(message.chat.id, meme_img)

        # конец блока отправки пользователю рандомного мема
        # начало блока отправки пользователю рандомного смайла

        elif message_from_user == 'Смайл 🤗':
            from smiles import smile_list

            bot.send_message(message.chat.id, '{0.first_name}, высылаю Вам рандомный смайл'.format(message.from_user))
            bot.send_message(message.chat.id, choice(smile_list))

        # конец блока отправки пользователю рандомного смайла
        # начало блока отправки пользователю содержимого загадочной коробки ахах

        elif message_from_user == 'Что в коробке? 📦':
            bot.send_message(message.chat.id, 'В коробке вишняяя🍒 йохуууууу')

            with open('photos/cherry.jpg', 'rb') as surprise:
                bot.send_photo(message.chat.id, surprise)

        # конец блока отправки пользователю содержимого загадочной коробки ахах
        # начало блока отправки пользователю стикера

        elif message_from_user == 'Стикер 😉':
            bot.send_message(message.chat.id, 'Вот так разработчик трудился при создании этого бота:')
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAECyXVhIUqD1OHkNiSNe-8tcA_S82KZGgACIAkAAhhC7gjhiiCooToK2SAE')

        # конец блока отправки пользователю стикера
        # начало блока, содержащего дополнительную информацию

        elif message_from_user == 'ℹ Информация ℹ':  # общий раздел с кнопками информации
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            markup.add(types.KeyboardButton('О боте 🤖'), types.KeyboardButton('О разработчике 👨🏼‍💻'))
            markup.add(types.KeyboardButton(back_button))

            bot.send_message(message.chat.id, '🟪 Чтобы узнать, как работают функции, выполняемые ботом, '
                                              'нажмите кнопку "<u>О боте</u> 🤖"\n\n'
                                              '🟪 Чтобы получить дополнительную информацию о разработчике, нажмите '
                                              'кнопку "<u>О разработчике</u> 👨🏼‍💻"',
                             reply_markup=markup, parse_mode='HTML')

        elif message_from_user == 'О боте 🤖':  # кнопка "О боте 🤖"
            bot.send_message(message.chat.id, 'Данный бот предоставляет вам различную информацию и '
                                              'состоит из следующих пунктов меню:\n\n➖➖❗  ⬇️   ⬇️  🔥  ⬇️   ⬇️  ❗➖➖\n\n'
                                              '▪️ пункт <b>"🔸 Рандомное число 🔸"</b> генерирует случайное число'
                                              ' из отрезка [0; 1000];\n\n'
                                              '▪️ пункт <b>"💸 Курсы валют 💸"</b> показывает текущее состояние выбранной'
                                              ' вами валюты на бирже по данным с сайта <a href="https://cbr.ru">'
                                              'ЦБ РФ</a>;\n\n'
                                              '▪️ пункт <b>"Города 🏙"</b> показывает местное время в городе '
                                              'и отправляет фото данного города в зависимости от '
                                              'времени суток по данным с сайта '
                                              '<a href="https://time.is/">Time.is</a>;\n\n'
                                              '▪️ пункт <b>"Мем 😀"</b> отправляет рандомный мем на IT тематику '
                                              'по данным с сайта <a href="https://bookflow.ru/it-shutki-pro-programmistov-yumor-razrabotchikov/">BookFlow</a>;\n\n'
                                              '▪️ пункт <b>"Смайл 🤗"</b> отправляет рандомный смайл;\n\n'
                                              '▪️ пункт <b>"Что в коробке? 📦"</b> показывает содержимое секретной '
                                              'коробки;\n\n'
                                              '▪️ пункт <b>"Стикер 😉"</b> отправляет пользователю стикер и всеобъемлюще'
                                              ' демонстрирует работу большинства программистов 😊;\n\n'
                                              '▪️ пункт <b>"ℹ Информация ℹ"</b> предоставляет дополнительную '
                                              'информацию о боте 🤖 и его разработчике 👨🏼‍💻.\n\n',
                             parse_mode='HTML')

        elif message_from_user == 'О разработчике 👨🏼‍💻':  # кнопка "О разработчике 👨🏼‍💻"
            markup = types.InlineKeyboardMarkup()

            markup.add(
                types.InlineKeyboardButton('Telegram', url='t.me/shvetsov_07'),
                types.InlineKeyboardButton('VK', url='https://vk.com/danilshvetsov07'),
                types.InlineKeyboardButton('Instagram', url='https://instagram.com/shvetsov_07?r=nametag')
            )

            bot.send_message(message.chat.id, '▪️Создатель / разработчик данного бота:\n'
                                              '️<i>Shvetsov Danil</i> 👨🏼‍💻\n\n▪️Он студент первого '
                                              'курса факультета компьютерных наук ВШЭ 🏫 🎓\n\n'
                                              '▪️Вот его фото, а также ссылки на <i>Telegram</i>, <i>VK</i> и '
                                              '<i>Instagram</i>:\n',
                             parse_mode='HTML')

            with open('photos/my_photo.jpg', 'rb') as my_photo:
                bot.send_photo(message.chat.id, my_photo, '\n', reply_markup=markup)

        # конец блока, содержащего дополнительную информацию
        # начало блока с кнопкой назад, которая возвращает пользователя в основное меню

        elif message_from_user == back_button:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            main_menu_buttons = ['🔸 Рандомное число 🔸', '💸 Курсы валют 💸', 'Города 🏙', 'Мем 😀', 'Смайл 🤗',
                                 'Что в коробке? 📦', 'Стикер 😉', 'ℹ Информация ℹ']
            for button in main_menu_buttons:
                markup.add(types.KeyboardButton(button))

            bot.send_message(message.chat.id, '{0.first_name}, выберите любую из предложенных'
                                              ' кнопок'.format(message.from_user), reply_markup=markup)

        # конец блока с кнопкой назад, которая возвращает пользователя в основное меню


bot.polling(none_stop=True)
