import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO user (email) VALUES (?)",
            ('grace@gmai.com',))


cur.execute("INSERT INTO BookTable (Title, Author, Genre) VALUES (?, ?, ?)",
            ("The Hobbit","J.R.R Tolkien", "Fiction"))

connection.commit()
connection.close()