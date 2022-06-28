import sqlite3

class BotDB:
	def __init__(self, db_file):
		"""Иницилизация соединения с БД"""
		self.conn = sqlite3.connect(db_file)
		self.cursor = self.conn.cursor()

	def user_exists(self, user_id):
		"""Проверяем, есть ли user в DB"""
		result = self.cursor.execute(f"SELECT id FROM users_data WHERE id = ?", (user_id,))
		return bool(len(result.fetchall()))

	def get_user_id(self, user_id):
		"""Получаем id юзерра в базе по его user_id в tg"""
		result = self.cursor.execute(f"SELECT id FROM users_data WHERE id", (user_id,))
		print(result.fetchone()[0])
		return result.fetchone()[0]

	def add_user(self, user_id, user_name):
		"""Добавить юзера"""
		self.cursor.execute(f"INSERT INTO users_data VALUES (?, ?, ?, ?)", (user_id, user_name, 0, 3))
		return self.conn.commit()

	def add_record(self, user_id, operation, value):
		"""Создать надпись о расходе/доходе"""
		self.cursor.execute(f"INSERT INTO records (id, operation, value) VALUES (?, ?, ?)",
			(self.get_user_id(user_id),
				operation == '+',
				value))
		return self.conn.commit()

	def close(self):
		self.conn.close()