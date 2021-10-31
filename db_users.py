import sqlite3


class BotDB:

    def __init__(self, db_file):
        """соединение с БД"""
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()

    def add_record(self, user_id, answer, question):
        """создаем запись запроса и ответа"""
        self.cursor.execute("INSERT INTO 'records' ('user_id', 'answer', 'question') VALUES (?, ?, ?)",
            (self.get_user_id(user_id), answer, question))
        return self.conn.commit()

    def close(self):
        self.conn.close()









