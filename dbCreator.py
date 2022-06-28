import sqlite3

db = sqlite3.connect('users_data.sqlite')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users_data (
	id BIGINT,
	user_name TEXT,
	balance BIGINT,
	usage INT
	)""")
db.commit()

sql.execute(f"INSERT INTO users_data VALUES (?, ?, ?, ?)", (410981657, 'dipperok', 0, -1))
db.commit()