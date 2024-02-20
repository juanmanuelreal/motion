# Importamos libreria
import sqlite3

# Crear conexión
connection = sqlite3.connect('motion.db')

# Crear cursor
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

# Confirmar cambios
connection.commit()

# Cerrar la conexión
connection.close()