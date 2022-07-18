import telebot
import config
from func_bot.weather import Weather
from func_bot.calculator import Calculator
from telebot import types


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def message_start(message):
    """Обработка /start и добавление клавиатуры"""
    sti = open('stickers/welcome.webp', 'rb')  # Элемент sti будет иметь стикер
    sti1 = open('stickers/hellome.webp', 'rb')  # Элемент sti1 будет иметь стикер

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)  # Размерности кнопок
    help_button = types.KeyboardButton('/help')  # Кнопка клавиатуры
    skills = types.KeyboardButton('Что умеешь?')
    markup.add(help_button, skills)  # Добавление и порядок кнопок

    if message.from_user.username == 'saynaraaye':  # Приветствие для Саши
        bot.send_sticker(message.chat.id, sti)  # Бот отправляет стикер
        bot.send_message(message.chat.id, 'Привет, <b>Сашка</b>\n'  # Бот отправляет сообщение
                                          'Кстати пошел нахер (;\n'
                                          'можешь посчитать свои циферки',
                         parse_mode='html', reply_markup=markup)  # Добавляем оформление и кнопки
    elif message.from_user.username == 'SnowBadger711':  # Приветствие для создателя с теми же функциями
        bot.send_sticker(message.chat.id, sti1)
        bot.send_message(message.chat.id, 'Царь-Бог прибыл!!!', parse_mode='html', reply_markup=markup)
    else:  # Приветствие для всех с теми же функциями
        bot.send_sticker(message.chat.id, sti)
        mess = f'Привет, <b>{message.from_user.username}</b>'
        bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
    if message.chat.id != '573154086':  # Если отправитель не создатель
        bot.send_message('573154086', f'Зашел: {message.from_user.username}')  # Пишет создателю кто зашел


@bot.message_handler(commands=['help'])  # Обработка /help и добавление кнопок
def message_help(message):
    """Обработчик /help и добавление кнопок"""
    first_name = f'{message.from_user.first_name}'  # Считываем имя
    last_name = f'{message.from_user.last_name}'  # Считываем фамилия

    if first_name != 'None' and last_name != 'None':  # Если есть имя и фамилия
        mess = 'Тебя зовут: ' + first_name + ' ' + last_name  # Записываем приветствием
    elif first_name != 'None' and last_name == 'None':  # Если есть имя и  нет фамилии
        mess = 'Тебя зовут: ' + first_name  # Записываем приветствием
    elif first_name == 'None' and last_name != 'None':  # Если нет имени и фамилии
        mess = 'Тебя зовут: ' + last_name  # Записываем приветствием
    else:
        mess = "У тебя нет имени?\n" \
               "Добавь его в Телеграм,\n" \
               "чтоб я знал как к тебе обращаться (:"  # Записываем обращение

    markup = types.InlineKeyboardMarkup()  # Объявление кнопок под сообщением
    user_id = types.InlineKeyboardButton('Мой ID', callback_data='id')  # Создаем кнопку с обращением 'id'
    markup.row(user_id)  # Добавляем первую линию кнопок

    cite = types.InlineKeyboardButton('Перейти на сайт',  # Кнопка с переходом на сайт
                                      url='https://www.youtube.com/shorts/gCSCOvSTV0c')
    markup.row(cite)  # Добавляем вторую линию кнопок

    bot.send_message(message.chat.id, mess, reply_markup=markup)  # Отправляем сообщение с кнопками


@bot.message_handler(commands=['clear'])  # Обработка /clear
def clear_msg(message):
    """Обработка /clear"""
    bot.delete_message(message.chat.id, message.message_id)  # Удаляем сообщение /clear
    bot.delete_message(message.chat.id, message.message_id - 1)  # Удаляет "Не понял тебя"
    bot.delete_message(message.chat.id, message.message_id - 2)  # Удаляет нераспознанное сообщение


@bot.message_handler(func=lambda message: message.text == 'Что умеешь?')
def skills_bot(message):
    """Обработчик сообщение 'Что умеешь?'
    Удаляет сообщение с вопросом, создает под клавиатурные кнопки"""
    bot.delete_message(message.chat.id, message.message_id)  # Удаляет сообщение 'Что делаешь?'
    sti = open('stickers/skills.webp', 'rb')  # Присваиваем стикер
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)  # Объявляем кнопки и задаем размеры
    weather = types.KeyboardButton('Погода')  # Под клавиатурная кнопка "Погода"
    calculator = types.KeyboardButton('Калькулятор')  # Под клавиатурная кнопка "Калькулятор"
    markup.add(weather, calculator)  # Создаем кнопки и задаем порядок
    bot.send_sticker(message.chat.id, sti, reply_markup=markup)  # Отправляем стикер и создаем кнопки
    bot.send_message(message.chat.id, 'Так-так-так, что у нас тут')  # Отправляем сообщение


@bot.message_handler(func=lambda message: message.text == 'Погода')
def get_city_for_weather(message):
    """Обработчик 'Погода' просит ввести город и даёт варианты ввиде кнопок
    выдает погоду, при новом запросе стирает её"""
    giv_city = Weather(bot)  # Создаём объект класса погода передаём бота
    giv_city.get_city_for_weather(message)  # Вызываем обработчик погоды передаём сообщение


@bot.message_handler(func=lambda message: message.text == 'Калькулятор')  # Просим ввести арифметический знак
def start_calculator(message):
    """Обработчик 'Калькулятор' просит ввести действие
    передает его в для выполнения действия"""
    calcul = Calculator(bot)  # Создаём объект класса калькулятор передаём бота
    calcul.start_calculator(message)  # Вызываем обработчик погоды передаём сообщение


@bot.message_handler()
def not_understand(message):
    """Обработчик сообщений
    ID пользователя по запросу, приветствие, нераспознанное сообщение"""
    hello = ['Привет', 'Привет)', 'Здравствуй', 'Здравствуй)', 'Приветик', 'Приветик)']
    if message.text.lower() == 'мой ID' or message.text.lower() == 'id' or message.text.lower() == 'my id':
        bot.send_message(message.chat.id, message.from_user.id)  # Отправляет ID по запросу
    elif message.text in hello:  # Если сообщением было приветствие отвечает взаимностью
        bot.send_message(message.chat.id, 'Привет)')
    else:  # Ответ на незарегистрированное сообщение
        sti = open('stickers/nounderstand.webp', 'rb')  # Создаем стикер для ответа

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Объявление кнопки и настройка размерности
        clear_message = types.KeyboardButton('/clear')  # Создание кнопки очистки
        markup.add(clear_message)  # Добавление кнопки

        bot.send_message(message.chat.id, 'Не понял тебя', reply_markup=markup)  # Вывод сообщения с кнопкой


@bot.callback_query_handler(func=lambda call: True)  # Обработчик кнопок Inline
def callback_inline(call):
    """Обработчик callback, подстрочных кнопок(под сообщением)"""
    if call.data == 'id':  # Распознание запроса и ответ на него
        bot.send_message(call.message.chat.id, f'<b>Твой ID</b>: <u>{call.from_user.id}</u>', parse_mode='html')
    else:  # Заготовка для будущих кнопок через elif
        pass


bot.polling(none_stop=True)
