import sqlite3

from fuzzywuzzy import fuzz
from fuzzywuzzy import process


class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def answer_question(self, question):
        """Ответ на вопрос"""
        #Вопрос юзера к нижнему регистру
        question = question.lower()
        #Получаем список вопросов и их id
        list_question = self.cursor.execute("SELECT `id`, `question` FROM `questions` ").fetchall()

        #Схожесть
        max_ratio = 0
        #id записи в БД
        id = 0

        #Проверяем каждый вопрос из БД
        for row in list_question:
            str = row[1]
            #Есть ли разделение в вопросе через;
            if str.find(";") != -1:
                list = str.split(';')
                for row_str in list:
                    ratio = fuzz.WRatio(question, row_str)
                    if ratio > max_ratio:
                        max_ratio = ratio
                        id = row[0]
            else:
                ratio = fuzz.WRatio(question, row[1])
                if ratio > max_ratio:
                    max_ratio = ratio
                    id = row[0]

        #Получение ответа из БД по id
        result = self.cursor.execute("SELECT `answer` FROM `questions` WHERE `id` = ?", (id,))
        return result.fetchall()

    def answer_question_by_id(self, id):
        """Получение записи"""
        result = self.cursor.execute("SELECT * FROM `questions` WHERE `id` = ?", (id,))
        return result.fetchall()

    def delete_answer_question(self, id):
        """Удаление записи"""
        self.cursor.execute("DELETE FROM `questions` WHERE `id` = ?", (id,))
        return self.conn.commit()

    def delete_user(self, id):
        """Удаление записи"""
        self.cursor.execute("DELETE FROM `users` WHERE `user_id` = ?", (id,))
        return self.conn.commit()

    def add_answer_question(self, question, answer):
        """Добавление вопроса-ответа в базу"""
        self.cursor.execute("INSERT INTO `questions` (`question`,'answer') VALUES (?, ?)", (question, answer,))
        return self.conn.commit()

    def add_user2(self, user_id, selected_student_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `users` (`user_id`,'selected_student_id') VALUES (?, ?)",
                            (user_id, selected_student_id,))
        return self.conn.commit()

    def find_user(self, name):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `students` WHERE `name` = ?", (name,))
        return int(len(result.fetchall()))

    def find_user2(self, name):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `students` WHERE `name` = ?", (name,))
        return result.fetchone()[0]

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def get_group_by_user_id(self, user_id):
        """Достаем группу из базы по user_id"""
        result = self.cursor.execute("SELECT g.name "
                                     "FROM groups g INNER JOIN students s on s.group_id = g.id "
                                     "INNER JOIN users u on u.selected_student_id = s.id "
                                     "WHERE u.user_id = ?", (user_id,))
        return result.fetchone()[0]

    def get_user_id(self, user_id):
        """Достаем юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def get_name_user_by_id(self, user_id):
        """Достаем имя юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT students.name "
                                     "FROM students INNER JOIN users ON users.selected_student_id = students.id "
                                     "WHERE users.user_id = ?", (user_id,))
        return result.fetchone()

    def get_students(self, name):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT students.name "
                                     "FROM students INNER JOIN groups ON groups.id = students.group_id "
                                     "WHERE groups.name = ?", (name,))
        return result.fetchall()

    def get_groups(self):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT name FROM groups")
        return result.fetchall()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
