import sqlite3

class DB():
  DB_NAME = "src/db/db.sqlite"

  def __init__(self):
    self.conn = sqlite3.connect(self.DB_NAME)
    self.cursor = self.conn.cursor()
    self.create_tables()
    print("Connected and created tables!")

  def create_tables(self):
      # create table user_data
      self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE
        )
      ''')

      # Create table - user_history
      self.cursor.execute('''
          CREATE TABLE IF NOT EXISTS user_history (
              id INTEGER PRIMARY KEY,
              user_id INTEGER,
              timestamp DATETIME NOT NULL,
              FOREIGN KEY(user_id) REFERENCES user_data(id) ON DELETE CASCADE
          )
      ''')


  def insert_user(self, username):
      if self.get_user_id(username) is None:
        self.cursor.execute('''
            INSERT INTO user_data (username) VALUES (?)
        ''', (username,))

      self.conn.commit()

  def get_user_id(self, username):
      self.cursor.execute('''
          SELECT id FROM user_data WHERE username = ?
      ''', (username,))

      query_result = self.cursor.fetchone()

      if query_result is None:
          return None

      return query_result[0]
  
  def insert_user_history(self, username, timestamp):
      user_id = self.get_user_id(username)
      self.cursor.execute('''INSERT INTO user_history (user_id, timestamp) VALUES (?, ?)''', (user_id, timestamp))
      self.conn.commit()


  def get_user_history(self):
      self.cursor.execute('''
          SELECT * FROM user_history
      ''')

      return self.cursor.fetchall()
  

  def __del__(self):
      print("Closing connection!")
      self.conn.close()
