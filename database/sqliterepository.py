from .model import Property
from .repository import AbstractRepository
from pathlib import Path
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

    @staticmethod
    def __create_connection(db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def __execute(conn, sql):
        try:
            c = conn.cursor()
            c.execute(sql)
            conn.commit()
            c.close()
        except Exception as e:
            print(e)

    @staticmethod
    def initialize_database(database='properties.db'):
        if Path(database).exists():
            raise FileExistsError(
                f"Database file {database} already exists; rename or delete")

        sql_create_properties_table = """ CREATE TABLE IF NOT EXISTS properties (
                                            id integer PRIMARY KEY,
                                            internal_id text NOT NULL,
                                            provider text NOT NULL,
                                            url text NOT NULL,
                                            captured_date integer DEFAULT CURRENT_TIMESTAMP
                                        ); """

        sql_create_index_on_properties_table = """ CREATE INDEX properties_internal_provider ON properties (internal_id, provider); """

        # create a database connection
        conn = SqliteRepository.__create_connection(database)
        with conn:
            if conn is not None:
                # create properties table
                SqliteRepository.__execute(conn, sql_create_properties_table)
                # create properties indexes
                SqliteRepository.__execute(
                    conn, sql_create_index_on_properties_table)
            else:
                print("Error! cannot create the database connection.")
