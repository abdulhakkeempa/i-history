class Table:
    def __init__(self, db_connection):
        self.db = db_connection

    def create(self):
        raise NotImplementedError

    def insert(self, data):
        raise NotImplementedError

    def fetch(self):
        raise NotImplementedError
