import requests
from func_bot.service import Service
from config import open_weather_token
from telebot import types
from deep_translator import GoogleTranslator


class Weather(Service):

    def get_city_for_weather(self, message) -> None:
        """Читаем и передаем город для вывода погоды"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # Объявляем кнопки и задаем размеры
        stop = types.KeyboardButton('/stop')  # Под клавиатурная кнопка "/stop"
        city_yar = types.KeyboardButton('Ярославль')  # Под клавиатурная кнопка "Ярославль"
        city_mos = types.KeyboardButton('Москва')  # Под клавиатурная кнопка "Москва"
        city_ny = types.KeyboardButton('Нью-Йорк')  # Под клавиатурная кнопка "Нью-Йорк"
        city_tok = types.KeyboardButton('Токио')  # Под клавиатурная кнопка "Токио"
        markup.add(city_yar, city_mos, city_ny, city_tok, stop)  # Создаем кнопки и задаем порядок

        self.bot.send_message(message.chat.id, 'В каком городе мне узнать погоду?', reply_markup=markup)
        self.bot.register_next_step_handler(message, self.get_weather)  # Читаем сообщение и передаем его в обработчик погоды
    
    def get_weather(self, message):  # Выдвет погоду по запросу
        self.bot.delete_message(message.chat.id, message.message_id)  # Удаляет сообщение с городом
        self.bot.delete_message(message.chat.id, message.message_id - 1)  # Удаляет сообщение с /stop
        if message.text == '/stop':  # Если сообщие было /stop
            self.stop_weather(message)  # Вызывает функцию /stop
            return  # Завершает функцию
        try:  # Проверка города
            geo = requests.get(  # Определяет данные полученного города
                f"http://api.openweathermap.org/geo/1.0/direct?q={message.text}&appid={open_weather_token}"
            )
            geo_data = geo.json()  # Записываем полученные данные
    
            name = GoogleTranslator(target='en').translate(geo_data[0]['name'])  # Переводим название города из данных
            city = GoogleTranslator(target='en').translate(message.text)  # Переводим город из сообщения
            if city.lower() != name.lower():  # Сравниваем названия если они разные
                self.bot.send_message(message.chat.id, f'Я не знаю город {message.text}')  # Сообщение об ошибке
                return  # Завершаем функцию
    
            lat = geo_data[0]["lat"]  # Определяем координаты
            lon = geo_data[0]["lon"]
    
            weather_geo = requests.get(  # По координатам берем погоду
                f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={open_weather_token}"
                f"&units=metric"
            )
            data = weather_geo.json()  # Записываем полученные данные
            temp = data["main"]["temp"]  # Запоминаем температура
            description = data["weather"][0]["description"]  # Запоминаем погодыне условия
            wind = data["wind"]["speed"]  # Запоминаем скорость ветра
    
            name = GoogleTranslator(target='ru').translate(name)  # Переводим название города
            description = GoogleTranslator(target='ru').translate(description)  # Переводим погодные условия
    
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # Созадем кнопки
            stop = types.KeyboardButton('/stop')  # Востанавливаем кнопки
            city_yar = types.KeyboardButton('Ярославль')
            city_mos = types.KeyboardButton('Москва')
            city_ny = types.KeyboardButton('Нью-Йорк')
            city_tok = types.KeyboardButton('Токио')
            markup.add(city_yar, city_mos, city_ny, city_tok, stop)  # Добавляем кнопки
    
            self.bot.send_message(message.chat.id, f"Город: <b>{name}</b>\n"  # Выводим полученную погоду
                                              f"Температура: <b>{temp}°C</b>\n"
                                              f"Погодные условия: <b>{description} над головой\n</b>"
                                              f"Скорость ветра: <b>{wind}м/с</b>\n"
                                              f"***Хорошего дня!***", parse_mode='html', reply_markup=markup)
    
        except Exception as ex:  # Если была ошибка
            print(ex)
            self.bot.send_message(message.chat.id, f'Я не знаю город {message.text}')  # Сообщаем об ошибке
        finally:  # В любом случае предлагаем закончить узнавать погоду
            self.bot.send_message(message.chat.id, 'Для того чтоб закончить узнавать погоду напиши\n'
                                                   '*/stop*')
            self.bot.register_next_step_handler(message, self.stop_weather)  # Передаем сообщение в разветвитель

    def stop_weather(self, message):
        """Заканчивает или продолжает работу с погодой"""
        if message.text == '/stop':  # Если сообщение было
            self.bot.delete_message(message.chat.id, message.message_id)  # Удаляет сообщение '/stop'
            self.bot.delete_message(message.chat.id, message.message_id - 1)  # Удаляет сообщение с /stop
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # Объявляем кнопки и размерность
            help_button = types.KeyboardButton('/help')  # Кнопки help и Что умеешь?
            question = types.KeyboardButton('Что умеешь?')
            markup.add(help_button, question)  # Создаем кнопки и их порядок
    
            self.bot.send_message(message.chat.id, 'Что дальше?)', reply_markup=markup)  # Выводим сообщение с кнопками
        else:
            self.get_weather(message)  # Запускаем обработчик погоды
