from telebot import types


class Calculator:

    def __init__(self, bot) -> None:
        self.bot = bot

    def start_calculator(self, message):
        """Обработчик 'Калькулятор' просит ввести действие
        передает его в для выполнения действия"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # Создаем под клавиатурные кнопки действия
        plus = types.KeyboardButton('+ (сложение)')  # Кнопка сложения
        minus = types.KeyboardButton('- (вычитание)')  # Кнопка вычитание
        division = types.KeyboardButton('/ (деление)')  # Кнопка деление
        multiply = types.KeyboardButton('* (умножение)')  # Кнопка умножение
        markup.add(plus, minus, division, multiply)  # Добавляем кнопки в определенном порядке

        self.bot.send_message(message.chat.id, 'Давай посчитаем, выбери действие', reply_markup=markup)  # Сообщение с кнопками
        self.bot.register_next_step_handler(message, self.get_action)  # Передаем прочитанное действие в калькулятор

    def get_action(self, message, total=None):
        """Распознаёт действие по первому символу
        Если это равенство пишет результат и даёт дальнеййшие возможные варианты в виде кнопок
        Если действие передаёт его в функцию подсчёта"""
        action_arr = ['+', '-', '/', '*', '=']  # Набор возможных действий
        action = message.text[0]
        if action == action_arr[-1]:  # Если действие '='
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # Объявляем кнопки возможного продолжения
            weather = types.KeyboardButton('Погода')  # Кнопка Погоды
            calculator = types.KeyboardButton('Калькулятор')  # Кнопка Калькулятор
            help_msg = types.KeyboardButton('/help')  # Кнопка help

            markup.add(weather, calculator, help_msg)  # Создаём и задаем их порядок

            self.bot.send_message(message.chat.id, f"Вот твой результат: {total}", reply_markup=markup)  # Отправка сообщения
        elif action in action_arr and total is not None:  # Если действие и вычисления были
            self.bot.send_message(message.chat.id, "Напиши число")  # Просим ввести число
            self.bot.register_next_step_handler(message, self.action_calculator, action, total)  # Передаем его в функцию подсчёта вместе с действием
        elif action in action_arr:  # Если действие и вычислений не было
            self.bot.send_message(message.chat.id, "Напиши 2 числа через пробел")  # Просим ввести 2 числа
            self.bot.register_next_step_handler(message, self.action_calculator, action)  # Передаём числа и действие в функцию подсчёта
        else:  # Если действия не было, выводим сообщение и приводим пример написания
            self.bot.send_message(message.chat.id, 'Не вижу арифметического действия, что нужно сделать?\n'
                                                   'Пример: "+"')
            self.bot.register_next_step_handler(message, self.get_action, total)  # Запускаем функцию заново, сохраняем текущий рузельтат

    def action_calculator(self, message, action, result=None):
        """Основная функция подсчёта чисел.
        Получает число(а), действие, текущий результат"""
        if result is None:  # Если вычислений не было спрашиваем 2 числа и запоминаем их
            try:  # Проверка чисел
                numbers = message.text.split(' ')  # Находим числа в сообщении и запоминаем их
                num1 = float(numbers[0])
                num2 = float(numbers[1])
            except Exception as ex:  # Если была допущена ошибка сообщаем о проблеме
                print(ex)
                self.bot.send_message(message.chat.id, 'Что-то не так с числами((\n'  # Просим ввести числа заново
                                                       'Напиши их заново')
                self.bot.register_next_step_handler(message, self.action_calculator, action, result)  # Вызываем функцию заново
                return  # Завершаем функцию в случае допущения ошибки
        else:  # Если вычисления были спрашиваем 1 число
            try:  # Проверка числа
                numbers = message.text.split(' ')  # Находим число
                num1 = result  # Берем результат предыдущего действия
                num2 = float(numbers[0])  # Запоминаем новое число
            except Exception as ex:  # Если была допущена ошибка сообщаем о проблеме
                print(ex)
                self.bot.send_message(message.chat.id, 'Что-то не так с числом((\n'  # Просим ввести число заново
                                                       'Напиши его заново')
                self.bot.register_next_step_handler(message, self.action_calculator, action, result)  # Вызываем функцию заново
                return  # Завершаем функцию в случае допущения ошибки

        if action == '+':  # Выполнение сложения
            self.bot.send_message(message.chat.id, "Складываю")
            result = num1 + num2
        elif action == '-':  # Выполнение вычитания
            self.bot.send_message(message.chat.id, "Вычитаю")
            result = num1 - num2
        elif action == '/' and num2 != 0:  # Выполнение деления, проверка на 'int / 0'
            self.bot.send_message(message.chat.id, "Делю")
            result = num1 / num2
        elif action == '*':  # Выполнение умножения
            self.bot.send_message(message.chat.id, "Умножаю")
            result = num1 * num2
        else:  # Если была предполагалось деление на 0
            self.bot.send_message(message.chat.id, 'На 0 делеить нельзя')
            result = 0

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # Обявление кнопок
        plus = types.KeyboardButton('+ (сложение)')  # Кнопки действий
        minus = types.KeyboardButton('- (вычитание)')
        division = types.KeyboardButton('/ (деление)')
        multiply = types.KeyboardButton('* (умножение)')
        answer = types.KeyboardButton('= (вычислить)')  # Добавление кнопки вычислить
        markup.add(plus, minus, division, multiply, answer)  # Добавление кнопок и их порядок

        self.bot.send_message(message.chat.id, f"Ваш промежуточный результат: <b>{result}</b>", parse_mode='html',
                              reply_markup=markup)  # Вывод результата и кнопок
        self.bot.register_next_step_handler(message, self.get_action, result)  # Передача сообщения в обработчик
