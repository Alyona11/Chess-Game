import mysql.connector
import datetime

HOST = '127.0.0.1'
USER = 'root'
PASSWORD = 'root'
SCHEMA = 'chess'


class Repository(object):

    # Відкрити connection з базою даних
    def __init__(self):
        self.connection = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWORD, database=SCHEMA, raise_on_warnings=True)

    # Метод для збереження гри в базу даних
    def save_game(self, name, activity):
        cursor = self.connection.cursor()  # Почати роботу з базою даних
        sql = "INSERT INTO games (name, activity, date) VALUES (%s, %s, %s)"
        values = (name, activity, datetime.datetime.now())
        cursor.execute(sql, values)  # Виконати SQL запит
        self.connection.commit()  # Підтвердити виконання SQL запиту
        cursor.close()  # Завершити роботу з базою даних

    # Метод для знаходження гри за її ім'ям
    def get_game(self, name):
        cursor = self.connection.cursor()  # Почати роботу з базою даних
        sql = "SELECT activity FROM games WHERE name = %s"
        value = (name,)
        cursor.execute(sql, value)  # Виконати SQL запит
        game_activity = cursor.fetchone()  # Вибрати один запис знайдений в базі даних за запитом
        cursor.close()  # Завершити роботу з базою даних
        return game_activity

    # Метод для знаходження всіх збережених ігор
    def get_games(self):
        cursor = self.connection.cursor()  # Почати роботу з базою даних
        sql = "SELECT name, date FROM games"
        cursor.execute(sql)  # Виконати SQL запит
        games = cursor.fetchall()  # Вибрати всі записи знайдені в базі даних за запитом
        cursor.close()  # Завершити роботу з базою даних
        return games
