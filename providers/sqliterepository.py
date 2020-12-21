from .model import Property
from .repository import AbstractRepository
import sqlite3


class SqliteRepository(AbstractRepository):

    def __init__(self, path_to_db):
        self.conn = sqlite3.connect(path_to_db)

    def add(self, prop):
        stmt = 'INSERT INTO properties (internal_id, provider, url) VALUES (:internal_id, :provider, :url)'
        self.conn.execute(stmt, prop)
        self.conn.commit()

    def get(self, internal_id, provider) -> Property:
        stmt = 'SELECT * FROM properties WHERE internal_id=:internal_id AND provider=:provider'
        cur = self.conn.cursor()
        cur.execute(
            stmt, {'internal_id': internal_id, 'provider': provider})
        result = cur.fetchone()
        cur.close()
        return result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
