from database import DatabaseConnection
from user_data import UserData
from user_history import UserHistory

class DB:
    DB_NAME = "src/db/db.sqlite"

    def __init__(self):
        self.db = DatabaseConnection(self.DB_NAME)
        self.user_data = UserData(self.db)
        self.user_history = UserHistory(self.db)
        self.create_tables()

    def create_tables(self):
        self.user_data.create()
        self.user_history.create()

    def insert_user(self, username):
        if self.get_user_id(username) is None:
            self.user_data.insert(username)
        self.db.commit()

    def get_user_id(self, username):
        return self.user_data.fetch(username)

    def insert_user_history(self, username, timestamp):
        user_id = self.get_user_id(username)
        self.user_history.insert(user_id, timestamp)
        self.db.commit()

    def get_user_history(self):
        return self.user_history.fetch()
