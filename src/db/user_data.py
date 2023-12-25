from table import Table

class UserData(Table):
    def create(self):
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS user_data (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE
            )
        ''')

    def insert(self, username):
        self.db.execute('''
            INSERT INTO user_data (username) VALUES (?)
        ''', (username,))

    def fetch(self, username):
        self.db.execute('''
            SELECT id FROM user_data WHERE username = ?
        ''', (username,))
        return self.db.fetchone()
