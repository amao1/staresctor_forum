import sqlite3

connection = sqlite3.connect('data.db')

cur = connection.cursor()

with open('schema.sql', 'r') as f:
    schema_sql = f.read()
cur.executescript(schema_sql)


#cur.execute("INSERT INTO users ()")

connection.commit()
connection.close()

