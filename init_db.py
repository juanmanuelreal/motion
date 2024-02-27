# Import library
import sqlite3

# Create connection
connection = sqlite3.connect('motion.db')

# Create cursor
cur = connection.cursor()

cur.execute("""CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)""")

cur.execute("""CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author TEXT NOT NULL,
    title TEXT NOT NULL,
    text TEXT NOT NULL
)""")

# Confirm changes
connection.commit()

# Close connection
connection.close()