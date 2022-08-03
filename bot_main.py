import telebot
import config
from message_text import MESSAGE_TEXT
from func_bot.weather import Weather
from func_bot.calculator import Calculator
from telebot import types
from bd_func.bd_record import BDRecord


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def message_start(message):
    """Обработка /start и добавление клавиатуры"""
    sticker = open('stickers/welcome.webp', 'rb')  # Создаем стикеры для ответа
    sticker1 = open('stickers/hellome.webp', 'rb')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)  # Размерности кнопок
    help_button = types.KeyboardButton('/help')  # Кнопка клавиатуры
    skills = types.KeyboardButton('Что умеешь?')
    markup.add(help_button, skills)  # Добавление и порядок кнопок

    bd = BDRecord()
    tg_user = bd.hello_user(message)

    if message.from_user.id == config.admin_id:  # Приветствие для создателя с теми же функциями
        bot.send_sticker(message.chat.id, sticker1)
        bot.send_message(message.chat.id, MESSAGE_TEXT.MESSAGE_ME, parse_mode='html', reply_markup=markup)
    elif tg_user is False:  # Приветствуем и добавляем нового пользователя
        bot.send_sticker(message.chat.id, sticker)
        bot.send_message(message.chat.id, MESSAGE_TEXT.MESSAGE_NEW_USER)
        bot.register_next_step_handler(message, bot_add_user)
    else:  # Приветствие для знакомого пользователя
        bot.send_sticker(message.chat.id, sticker)
        bot.send_message(message.chat.id, f"Привет, <b>{tg_user[0]} {tg_user[1]}</b>", reply_markup=markup,
                         parse_mode='html')
        bd.get_date_user(message)

    if message.chat.id != '573154086':  # Если отправитель не создатель
        bot.send_message('573154086', f'Зашел: {message.from_user.username}')  # Пишет создателю кто зашел


def bot_add_user(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)  # Размерности кнопок
    help_button = types.KeyboardButton('/help')  # Кнопка клавиатуры
    skills = types.KeyboardButton('Что умеешь?')
    markup.add(help_button, skills)  # Добавление и порядок кнопок
    bd = BDRecord()
    bd.add_user(message)
    bot.send_message(message.chat.id, f"Отлично, {bd.get_user_bd(message.from_user.id)[0][1]}", reply_markup=markup)


@bot.message_handler(commands=['help'])
def message_help(message):
    """Обработчик /help и добавление кнопок"""
    bd = BDRecord()
    bd.get_date_user(message)
    first_name = f'{message.from_user.first_name}'  # Считываем данные пользователя
    last_name = f'{message.from_user.last_name}'

    if first_name != 'None' and last_name != 'None':  # В зависимости от данных выводим результат
        mess = 'Тебя зовут: ' + first_name + ' ' + last_name
    elif first_name != 'None' and last_name == 'None':
        mess = 'Тебя зовут: ' + first_name
    elif first_name == 'None' and last_name != 'None':
        mess = 'Тебя зовут: ' + last_name
    else:
        mess = MESSAGE_TEXT.MESSAGE_NO_NAME  # Записываем обращение

    markup = types.InlineKeyboardMarkup()  # Объявление кнопок под сообщением
    user_id = types.InlineKeyboardButton('Мой ID', callback_data='id')  # Создаем кнопку с обращением 'id'
    markup.row(user_id)  # Добавляем первую линию кнопок

    cite = types.InlineKeyboardButton('Перейти на сайт',  # Кнопка с переходом на сайт
                                      url='https://www.youtube.com/shorts/gCSCOvSTV0c')
    markup.row(cite)  # Добавляем вторую линию кнопок

    bot.send_message(message.chat.id, mess, reply_markup=markup)  # Отправляем сообщение


@bot.message_handler(commands=['clear'])
def clear_msg(message):
    """Обработчик /clear
    Удаляет 3 последних сообщения"""
    bot.delete_message(message.chat.id, message.message_id - 3)
    bot.delete_message(message.chat.id, message.message_id - 2)
    bot.delete_message(message.chat.id, message.message_id - 1)
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(commands=['admin'])
def admin(message):
    """Вывод всех данных БД для админа бота"""
    if message.from_user.id == config.admin_id:
        bd = BDRecord()
        bd_list = bd.get_all_bd()
        for row in bd_list:
            bot.send_message(message.chat.id, f"""ID: {row[0]}
Имя: {row[1]}
Фамилия: {row[2]}
Возраст: {row[3]}
Дата входа: {row[4]}""")
    else:
        bot.send_message(message.chat.id, 'Не воображай))')


@bot.message_handler(func=lambda message: message.text == 'Что умеешь?')
def skills_bot(message):
    """Обработчик сообщение 'Что умеешь?'
    Удаляет сообщение с вопросом, создает под клавиатурные кнопки"""
    bd = BDRecord()
    bd.get_date_user(message)
    bot.delete_message(message.chat.id, message.message_id)  # Удаляет сообщение 'Что делаешь?'
    sticker = open('stickers/skills.webp', 'rb')  # Присваиваем стикер
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)  # Объявляем кнопки и задаем размеры
    weather = types.KeyboardButton('Погода')  # Под клавиатурная кнопка "Погода"
    calculator = types.KeyboardButton('Калькулятор')  # Под клавиатурная кнопка "Калькулятор"
    markup.add(weather, calculator)  # Создаем кнопки и задаем порядок
    bot.send_sticker(message.chat.id, sticker, reply_markup=markup)  # Отправляем стикер и создаем кнопки
    bot.send_message(message.chat.id, MESSAGE_TEXT.MESSAGE_SKILLS)  # Отправляем сообщение


@bot.message_handler(func=lambda message: message.text == 'Погода')
def get_city_for_weather(message):
    """Обработчик 'Погода' просит ввести город и даёт варианты ввиде кнопок
    выдает погоду, при новом запросе стирает её"""
    bd = BDRecord()
    bd.get_date_user(message)
    giv_city = Weather(bot)  # Передаём бота
    giv_city.get_city_for_weather(message)  # Передаём сообщение


@bot.message_handler(func=lambda message: message.text == 'Калькулятор')
def start_calculator(message):
    """Обработчик 'Калькулятор' просит ввести действие
    передает его в для выполнения действия"""
    bd = BDRecord()
    bd.get_date_user(message)
    calcul = Calculator(bot)  # Передаём бота
    calcul.start_calculator(message)  # Передаём сообщение


@bot.message_handler()
def not_understand(message):
    """Обработчик сообщений
    ID пользователя по запросу, приветствие, нераспознанное сообщение"""
    bd = BDRecord()
    bd.get_date_user(message)
    if message.text.lower() == 'мой ID' or message.text.lower() == 'id' or message.text.lower() == 'my id':
        bot.send_message(message.chat.id, message.from_user.id)  # Отправляет ID по запросу
    elif message.text in MESSAGE_TEXT.MESSAGE_HELLO:  # Если сообщением было приветствие отвечает взаимностью
        bot.send_message(message.chat.id, 'Привет)')
    else:  # Ответ на незарегистрированное сообщение
        sticker = open('stickers/nounderstand.webp', 'rb')  # Создаем стикер для ответа

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Объявление кнопки и настройка размерности
        clear_message = types.KeyboardButton('/clear')
        markup.add(clear_message)

        bot.send_sticker(message.chat.id, sticker, reply_markup=markup)
        bot.send_message(message.chat.id, MESSAGE_TEXT.MESSAGE_NO_UNDERSTAND)  # Вывод сообщение


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """Обработчик callback, подстрочных кнопок(под сообщением)"""
    if call.data == 'id':  # Распознание запроса и ответ на него
        bot.send_message(call.message.chat.id, f'<b>Твой ID</b>: <u>{call.from_user.id}</u>', parse_mode='html')
    else:
        pass


bot.polling(none_stop=True)
