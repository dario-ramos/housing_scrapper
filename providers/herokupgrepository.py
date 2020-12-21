from .repository import AbstractRepository
from .model import Property
import os
import psycopg2


def getDbUriFromHeroku(heroku_app_name):
    return os.environ['DATABASE_URL']


class HerokuPgRepository(AbstractRepository):

    def __init__(self, db_uri):
        self.conn = psycopg2.connect(db_uri)

    def add(self, prop):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO properties (internal_id, provider, url) VALUES (%s, %s, %s)", prop)
        self.conn.commit()
        cur.close()

    def get(self, internal_id, provider) -> Property:
        cur = self.conn.cursor()
        stmt = 'SELECT * FROM properties WHERE internal_id=(%internal_id) AND provider=(%provider)'
        cur.execute(
            stmt, [internal_id, provider])
        result = cur.fetchone()
        cur.close()
        return result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
