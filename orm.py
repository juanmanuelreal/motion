import sqlite3

class Database:
    def __init__(self, name: str):
        print(f"Opening database in db_name: {name}")
        self.name = name
        
    def _get_db_connection(self):
        conn = sqlite3.connect(self.name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def query_all(self, query: str):
        try:
            conn = self._get_db_connection()
            query_result = conn.execute(query).fetchall() #query = "SELECT * from tabla"
            conn.close()
            return query_result
        except Exception as e:
            print(f"Fatal error during the inqury, error: {e}")
            raise
    
    def query_where(self, query: str, params: tuple):
        try:
            conn = self._get_db_connection()
            query_result = conn.execute(query, params).fetchall() # query = "SELECT * FROM tabla WHERE tabla.campo == ?" params = (params1,)
            conn.close()
            return query_result
        except Exception as e:
            print(f"Fatal error during the inqury, error: {e}")
            raise
    
    def insert(self, query: str, params: tuple):
        try:
            conn = self._get_db_connection()
            conn.execute(query, params) # query = 'INSERT INTO table ...'
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Fatal error during the inqury, error: {e}")
            raise

class User(Database):
    def get_user_by_username(self, username: str):
        try:
            query = "SELECT * FROM users WHERE users.username == ?"
            params = (username,)
            user = self.query_where(query, params)
            return user
        except Exception as e:
            raise

    def create_user(self, username: str, password: str):
        try:
            query = "INSERT INTO users (username, password) VALUES (?,?)"
            params = (username, password)
            self.insert(query, params)
        except Exception as e:
            raise

class Post(Database):
    def __init__(self, db_name):
        super().__init__(db_name)
    
    def get_all_posts(self):
        try:
            query = "SELECT * FROM posts"
            posts = self.query_all(query)
            return posts
        except Exception as e:
            raise
        
    def query_all(self, query):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_posts_by_id(self, id: str):
        try:
            query = "SELECT * FROM posts WHERE posts.id == ?"
            params = (id,)
            post = self.query_where(query, params)
            return post
        except Exception as e:
            raise

    def get_posts_by_title(self, title: str):
        try:
            query = "SELECT * FROM posts WHERE posts.titulo LIKE ?"
            params = (f"%{title}%",)
            posts = self.query_where(query, params)
            return posts
        except Exception as e:
            raise

    def create_post(self, author: str, title: str, text: str):
        try:
            query = "INSERT INTO posts (author, title, text) VALUES (?,?,?)"
            params = (author, title, text)
            self.insert(query, params)
        except Exception as e:
            raise