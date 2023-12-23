import sqlite3

class DB():
  DB_NAME = "db.sqlite3"

  def __init__(self):
    self.conn = sqlite3.connect('db.sqlite3')
    self.cursor = self.conn.cursor()
    self.create_tables()

  def create_tables(self):
      # create table user_data
      self.cursor.execute('''
        CREATE TABLE user_data (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
        )
      ''')

      # Create table - user_history
      self.cursor.execute('''
          CREATE TABLE user_history (
              id INTEGER PRIMARY KEY,
              user_id INTEGER,
              timestamp DATETIME NOT NULL,
              FOREIGN KEY(user_id) REFERENCES user_data(id) ON DELETE CASCADE
          )
      ''')


  def insert_user(self, username):
      self.cursor.execute('''
          INSERT INTO user_data (username) VALUES (?)
      ''', (username,))

      self.conn.commit()

  def get_user_id(self, username):
      self.cursor.execute('''
          SELECT id FROM user_data WHERE username = ?
      ''', (username,))

      return self.cursor.fetchone()[0]
  
  def insert_user_history(self, username, timestamp):
      user_id = self.get_user_id(username)
      self.cursor.execute('''INSERT INTO user_history (user_id, timestamp) VALUES (?, ?)''', (user_id, timestamp))
      self.conn.commit()


  def get_user_history(self):
      self.cursor.execute('''
          SELECT * FROM user_history
      ''')

      return self.cursor.fetchall()