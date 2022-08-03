from bd_func.bd import BDFunc
from datetime import datetime


class BDRecord:

    def __init__(self):
        """Открываем базу данных"""
        self.bd = BDFunc()

    def get_date_user(self, message):
        """Запись времени от последнего написанного сообщения"""
        self.bd.bd_update_date(message.from_user.id, datetime.today().strftime('%Y-%m-%d %H:%M'))

    def get_user_bd(self, id_user):
        """Получаем данные о пользователе через его id"""
        return self.bd.bd_get_user_id(id_user)

    def hello_user(self, message):
        """Получаем Имя и Фамилию пользователя для приветствия"""
        user = self.bd.bd_get_user_id(message.from_user.id)
        if user is not False:
            return user[0][1], user[0][2]
        else:
            return False

    def add_user(self, message):
        """Добавляем данные нового пользователя"""
        user = message.text.split()
        id_user = message.from_user.id
        try:
            first_name = user[0]
            last_name = user[1]
            age = user[2]
        except Exception as ex:
            print(ex)
            first_name = 'None'
            last_name = 'None'
            age = 0
        self.bd.bd_add_visitor(id_user, first_name, last_name, age)

    def get_all_bd(self):
        """Закрываем базу данных"""
        return self.bd.bd_all()


