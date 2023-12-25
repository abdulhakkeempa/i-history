from table import Table

class UserHistory(Table):
    def create(self):
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS user_history (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                timestamp DATETIME NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user_data(id) ON DELETE CASCADE
            )
        ''')

    def insert(self, user_id, timestamp):
        self.db.execute('''
            INSERT INTO user_history (user_id, timestamp) VALUES (?, ?)
        ''', (user_id, timestamp))

    def fetch(self, user_id):
        self.db.execute('''
            SELECT * FROM user_history WHERE user_id = ?
        ''', (user_id,))
        return self.db.fetchall()
