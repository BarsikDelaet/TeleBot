"""Функции калькулятора, считывает действие, выполняет его, дальше по кругу, пока не будет '=',
После предлагает повторить или перейти к другим функциям."""
__author__ = "Барсуков М.О."
from telebot import types
from func_bot.service import Service


class Calculator(Service):

    def start_calculator(self, message):
        """Обработчик 'Калькулятор' просит ввести действие
        передает его для выполнения."""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # Создаем под клавиатурные кнопки действия
        plus = types.KeyboardButton('+ (сложение)')
        minus = types.KeyboardButton('- (вычитание)')
        division = types.KeyboardButton('/ (деление)')
        multiply = types.KeyboardButton('* (умножение)')
        markup.add(plus, minus, division, multiply)

        self.bot.send_message(message.chat.id, 'Давай посчитаем, выбери действие', reply_markup=markup)  # Сообщение с кнопками
        self.bot.register_next_step_handler(message, self.get_action)  # Передаем прочитанное действие в калькулятор

    def get_action(self, message, total=None):
        """Распознаёт действие по первому символу
        Если это равенство пишет результат и даёт дальнейшие возможные варианты в виде кнопок
        Если действие передаёт его в функцию подсчёта"""
        action_arr = ['+', '-', '/', '*', '=']  # Набор возможных действий
        action = message.text[0]
        if action == action_arr[-1]:  # Если действие '=', выдаёт возможные варианты продолжения
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            weather = types.KeyboardButton('Погода')
            calculator = types.KeyboardButton('Калькулятор')
            help_msg = types.KeyboardButton('/help')
            markup.add(weather, calculator, help_msg)

            self.bot.send_message(message.chat.id, f"Вот твой результат: {total}", reply_markup=markup)
        elif action in action_arr and total is not None:  # Если действие и вычисления были
            self.bot.send_message(message.chat.id, "Напиши число")
            self.bot.register_next_step_handler(message, self.action_calculator, action, total)
        elif action in action_arr:  # Если действие и вычислений не было
            self.bot.send_message(message.chat.id, "Напиши 2 числа через пробел")
            self.bot.register_next_step_handler(message, self.action_calculator, action)
        else:  # Если действия не было, выводим сообщение и приводим пример написания
            self.bot.send_message(message.chat.id, 'Не вижу арифметического действия, что нужно сделать?\n'
                                                   'Пример: "+"')
            self.bot.register_next_step_handler(message, self.get_action, total)  # Запускаем функцию заново, сохраняем текущий результат

    def action_calculator(self, message, action, result=None):
        """Основная функция подсчёта чисел.
        Получает число(а), действие, текущий результат"""
        if result is None:  # Если вычислений не было спрашиваем 2 числа и запоминаем их
            try:  # Проверка чисел
                numbers = message.text.split(' ')
                num1 = float(numbers[0])
                num2 = float(numbers[1])
            except Exception as ex:  # Если была допущена ошибка сообщаем о проблеме
                print(ex)
                self.bot.send_message(message.chat.id, 'Что-то не так с числами((\n'
                                                       'Напиши их заново')
                self.bot.register_next_step_handler(message, self.action_calculator, action, result)
                return
        else:  # Если вычисления были спрашиваем 1 число
            try:  # Проверка числа
                numbers = message.text.split(' ')
                num1 = result
                num2 = float(numbers[0])
            except Exception as ex:  # Если была допущена ошибка сообщаем о проблеме
                print(ex)
                self.bot.send_message(message.chat.id, 'Что-то не так с числом((\n'
                                                       'Напиши его заново')
                self.bot.register_next_step_handler(message, self.action_calculator, action, result)
                return

        if action == '+':  # Выполнение действия
            self.bot.send_message(message.chat.id, "Складываю")
            result = num1 + num2
        elif action == '-':
            self.bot.send_message(message.chat.id, "Вычитаю")
            result = num1 - num2
        elif action == '/' and num2 != 0:
            self.bot.send_message(message.chat.id, "Делю")
            result = num1 / num2
        elif action == '*':
            self.bot.send_message(message.chat.id, "Умножаю")
            result = num1 * num2
        else:
            self.bot.send_message(message.chat.id, 'На 0 делить нельзя')
            result = 0

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # Объявление кнопок действия
        plus = types.KeyboardButton('+ (сложение)')
        minus = types.KeyboardButton('- (вычитание)')
        division = types.KeyboardButton('/ (деление)')
        multiply = types.KeyboardButton('* (умножение)')
        answer = types.KeyboardButton('= (вычислить)')
        markup.add(plus, minus, division, multiply, answer)

        self.bot.send_message(message.chat.id, f"Ваш промежуточный результат: <b>{result}</b>", parse_mode='html',
                              reply_markup=markup)  # Вывод результата и кнопок
        self.bot.register_next_step_handler(message, self.get_action, result)  # Передача сообщения в обработчик
