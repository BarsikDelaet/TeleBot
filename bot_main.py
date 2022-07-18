import telebot
import config
import requests
from config import open_waether_token
from telebot import types
from deep_translator import GoogleTranslator


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])  # Обработка /start и добавление клавиатуры
def message_start(message):
    sti = open('stickers/welcome.webp', 'rb')
    sti1 = open('stickers/helloasy.webp', 'rb')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)  # Размерности кнопок
    help_button = types.KeyboardButton('/help')
    skills = types.KeyboardButton('Что умеешь?')
    markup.add(help_button, skills)

    if message.from_user.username == 'saynaraaye':  # Приветствие для Саши
        bot.send_sticker(message.chat.id, sti)
        bot.send_message(message.chat.id, 'Привет, <b>Сашка</b>\n'
                                          'Кстати пошел нахер (;\n'
                                          'можешь посчитать свои циферки',
                         parse_mode='html', reply_markup=markup)
    elif message.from_user.username == 'SnowBadger711':  # Приветствие для создателя
        bot.send_sticker(message.chat.id, sti1)
        bot.send_message(message.chat.id, 'Царь-Бог прибыл!!!', parse_mode='html', reply_markup=markup)
    else:  # Приветствие для всех
        bot.send_sticker(message.chat.id, sti)
        mess = f'Привет, <b>{message.from_user.username}</b>'
        bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
    if message.chat.id != '573154086':
        bot.send_message('573154086', f'Зашел: {message.from_user.username}')


@bot.message_handler(commands=['help'])  # Обработка /help и добавление кнопок
def message_help(message):
    first_name = f'{message.from_user.first_name}'
    last_name = f'{message.from_user.last_name}'

    if first_name != 'None' and last_name != 'None':
        mess = 'Тебя зовут: ' + first_name + ' ' + last_name
    elif first_name != 'None' and last_name == 'None':
        mess = 'Тебя зовут: ' + first_name
    elif first_name == 'None' and last_name != 'None':
        mess = 'Тебя зовут: ' + last_name
    else:
        mess = 'У тебя нет имени?\n' \
               'Добавь его в Телеграм,\n' \
               'чтоб я знал как к тебе обращаться (:'

    markup = types.InlineKeyboardMarkup()  # Объявление кнопок
    user_id = types.InlineKeyboardButton('Мой ID', callback_data='id')
    markup.row(user_id)

    cite = types.InlineKeyboardButton('Перейти на сайт', url='https://www.youtube.com/shorts/gCSCOvSTV0c')
    markup.row(cite)

    bot.send_message(message.chat.id, mess, reply_markup=markup)


@bot.message_handler(commands=['clear'])  # Обработка /clear
def clear_msg(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    bot.delete_message(message.chat.id, message.message_id - 2)


@bot.message_handler(func=lambda message: message.text == 'Что умеешь?')  # Функция на "Что умеешь?"
def skills_bot(message):
    bot.delete_message(message.chat.id, message.message_id)
    sti = open('stickers/skills.webp', 'rb')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    weather = types.KeyboardButton('Погода')
    calculator = types.KeyboardButton('Калькулятор')
    markup.add(weather, calculator)
    bot.send_sticker(message.chat.id, sti, reply_markup=markup)
    bot.send_message(message.chat.id, 'Так-так-так, что у нас тут')


@bot.message_handler(func=lambda message: message.text == 'Погода')  # Читаем и передаем город для вывода погоды
def get_city_for_weather(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    stop = types.KeyboardButton('/stop')
    city_yar = types.KeyboardButton('Ярославль')
    city_mos = types.KeyboardButton('Москва')
    city_ny = types.KeyboardButton('Нью-Йорк')
    city_tok = types.KeyboardButton('Токио')
    markup.add(city_yar, city_mos, city_ny, city_tok, stop)

    bot.send_message(message.chat.id, 'В каком городе мне узнать погоду?', reply_markup=markup)
    bot.register_next_step_handler(message, get_weather)  # Передаем город в функцию вывода погоды


@bot.message_handler(func=lambda message: message.text == 'Калькулятор')  # Просим ввести арифметический знак
def start_calculator(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    plus = types.KeyboardButton('+ (сложение)')
    minus = types.KeyboardButton('- (вычитание)')
    division = types.KeyboardButton('/ (деление)')
    multiply = types.KeyboardButton('* (умножение)')
    markup.add(plus, minus, division, multiply)

    bot.send_message(message.chat.id, 'Давай посчитаем, выбери действие', reply_markup=markup)
    bot.register_next_step_handler(message, get_action)


@bot.message_handler()  # Обработчик сообщений
def not_understand(message):
    hello = ['Привет', 'Привет)', 'Здравствуй', 'Здравствуй)', 'Приветик', 'Приветик)']
    if message.text.lower() == 'мой ID' or message.text.lower() == 'id' or message.text.lower() == 'my id':
        bot.send_message(message.chat.id, message.from_user.id)
    elif message.text in hello:
        markup = types.ReplyKeyboardMarkup()
        markup.add()
        bot.send_message(message.chat.id, 'Привет)', reply_markup=markup)
    else:  # Ответ на незарегистрированное сообщение
        sti = open('stickers/nounderstand.webp', 'rb')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        clear_message = types.KeyboardButton('/clear')
        markup.add(clear_message)

        bot.send_message(message.chat.id, 'Не понял тебя', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)  # Обработчик кнопок Inline
def callback_inline(call):
    if call.data == 'id':  # Кнопки с /help
        bot.send_message(call.message.chat.id, f'<b>Твой ID</b>: <u>{call.from_user.id}</u>', parse_mode='html')
    elif call.data == 'SanyLox':  # Кнопки с непонятного сообщения
        sti = open('stickers/shalu.webp', 'rb')
        bot.send_sticker(call.message.chat.id, sti)
    elif call.data == 'help':
        bot.send_message(call.message.chat.id, 'Нажми */help*')
    else:
        pass


'''Функции погоды'''


def get_weather(message):  # Выдвет погоду по запросу
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    bot.delete_message(message.chat.id, message.message_id - 2)
    if message.text == '/stop':
        stop_weather(message)
        return
    try:
        geo = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={message.text}&appid={open_waether_token}"
        )
        geo_data = geo.json()

        name = GoogleTranslator(target='en').translate(geo_data[0]['name'])
        city = GoogleTranslator(target='en').translate(message.text)
        if city.lower() != name.lower():
            bot.send_message(message.chat.id, f'Я не знаю город {message.text}')
            return

        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]

        weather_geo = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={open_waether_token}"
            f"&units=metric"
        )
        data = weather_geo.json()
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        wind = data["wind"]["speed"]

        name = GoogleTranslator(target='ru').translate(name)
        description = GoogleTranslator(target='ru').translate(description)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        stop = types.KeyboardButton('/stop')
        city_yar = types.KeyboardButton('Ярославль')
        city_mos = types.KeyboardButton('Москва')
        city_ny = types.KeyboardButton('Нью-Йорк')
        city_tok = types.KeyboardButton('Токио')
        markup.add(city_yar, city_mos, city_ny, city_tok, stop)

        bot.send_message(message.chat.id, f"Город: <b>{name}</b>\n"
                                          f"Температура: <b>{temp}°C</b>\n"
                                          f"Погодные условия: <b>{description} над головой\n</b>"
                                          f"Скорость ветра: <b>{wind}м/с</b>\n"
                                          f"***Хорошего дня!***", parse_mode='html', reply_markup=markup)

    except Exception as ex:
        print(ex)
        bot.send_message(message.chat.id, f'Я не знаю город {message.text}')
    finally:
        bot.send_message(message.chat.id, 'Для того чтоб закончить узнавать погоду напиши\n'
                                          '*/stop*')
        bot.register_next_step_handler(message, stop_weather)


def stop_weather(message):  # Заканчивает или продолжает работу get_weather
    if message.text == '/stop':
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        help_button = types.KeyboardButton('/help')
        question = types.KeyboardButton('Что умеешь?')
        markup.add(help_button, question)

        bot.send_message(message.chat.id, 'Что дальше?)', reply_markup=markup)
    else:
        get_weather(message)


'''Функции калькулятора'''


def get_action(message, total=None):
    print(total)
    action_arr = ['+', '-', '/', '*', '=']
    if message.text[0] == action_arr[-1]:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        weather = types.KeyboardButton('Погода')
        calculator = types.KeyboardButton('Калькулятор')
        help_msg = types.KeyboardButton('/help')

        markup.add(weather, calculator, help_msg)

        bot.send_message(message.chat.id, f"Вот твой результат: {total}", reply_markup=markup)
    elif message.text[0] in action_arr and total is not None:
        print(total)
        action = message.text[0]
        bot.send_message(message.chat.id, "Напиши число")
        bot.register_next_step_handler(message, action_calculator, action, total)
    elif message.text[0] in action_arr:
        print(message.text)
        action = message.text[0]
        print(action)
        bot.send_message(message.chat.id, "Напиши 2 числа через пробел")
        bot.register_next_step_handler(message, action_calculator, action)
    else:
        bot.send_message(message.chat.id, 'Не вижу арифметического действия, что нужно сделать?')
        bot.register_next_step_handler(message, get_action, total)


def action_calculator(message, action, result=None):
    if result is None:
        try:
            numbers = message.text.split(' ')
            num1 = float(numbers[0])
            num2 = float(numbers[1])
        except Exception as ex:
            print(ex)
            bot.send_message(message.chat.id, 'Что-то не так с числами((\n'
                                              'Напиши их заново')
            bot.register_next_step_handler(message, action_calculator)
        numbers = message.text.split(' ')
        num1 = float(numbers[0])
        num2 = float(numbers[1])

    else:
        try:
            numbers = message.text.split(' ')
            num1 = float(numbers[0])
        except Exception as ex:
            print(ex)
            bot.send_message(message.chat.id, 'Что-то не так с числом((\n'
                                              'Напиши его заново')
            bot.register_next_step_handler(message, action_calculator, result)
        numbers = message.text.split(' ')

        num1 = result
        num2 = float(numbers[0])
    if action == '+':
        bot.send_message(message.chat.id, "Складываю")
        result = num1 + num2
    elif action == '-':
        bot.send_message(message.chat.id, "Вычитаю")
        result = num1 - num2
    elif action == '/' and num2 != 0:
        bot.send_message(message.chat.id, "Делю")
        result = num1 / num2
    elif action == '*':
        bot.send_message(message.chat.id, "Умножаю")
        result = num1 * num2
    else:
        result = 0
    print('1')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    plus = types.KeyboardButton('+ (сложение)')
    minus = types.KeyboardButton('- (вычитание)')
    division = types.KeyboardButton('/ (деление)')
    multiply = types.KeyboardButton('* (умножение)')
    answer = types.KeyboardButton('= (вычислить)')
    markup.add(plus, minus, division, multiply, answer)

    bot.send_message(message.chat.id, f"Ваш промежуточный результат: <b>{result}</b>", parse_mode='html',
                     reply_markup=markup)
    bot.register_next_step_handler(message, get_action, result)


bot.polling(none_stop=True)
