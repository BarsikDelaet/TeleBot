import psycopg2
from config import password_bd
from datetime import datetime


class BDFunc:

    def __init__(self):
        """Открытие БД"""
        self.con = psycopg2.connect(
            database="postgres",
            user="postgres",
            password=f"{password_bd}",
            host="127.0.0.1",
            port="5432"
        )

    def bd_add_visitor(self, id_user, first_name, last_name, age):
        """Добавляем нового посетителя"""
        cur = self.con.cursor()
        cur.execute(f"""INSERT INTO TG_USER 
            (ID_USER, FIRST_NAME, LAST_NAME, AGE, LAST_DATE) 
            VALUES({id_user}, '{first_name}', '{last_name}', {age}, '{datetime.today().strftime('%Y-%m-%d %H:%M')}')"""
                    )

        self.con.commit()

    def bd_update_date(self, id_user, last_date):
        """Обновляем время последнего входа посетителя"""
        cur = self.con.cursor()
        cur.execute(
            f"UPDATE TG_USER set LAST_DATE = '{last_date}' WHERE ID_USER = {id_user}")

        self.con.commit()

    def bd_all(self):
        """Вывод полного списка данных для Админа"""
        cur = self.con.cursor()
        cur.execute(
            "SELECT *"
            "FROM TG_USER")

        rows = cur.fetchall()
        return rows

    def bd_get_user_id(self, id_user):
        """Получаем данные по ользователю через его id"""
        cur = self.con.cursor()
        cur.execute(f"SELECT * FROM TG_USER WHERE id_user = {id_user}")

        user = cur.fetchall()
        if len(user) != 0:
            return user
        else:
            return False

    def __del__(self):
        """Закрываем БД"""
        self.con.commit()
        self.con.close()
