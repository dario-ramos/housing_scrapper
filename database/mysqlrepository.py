import pymysql
from .repository import AbstractRepository
from .model import Property


""" 
In this class, we open the connection to the database and never close it.
This is fine for a small app such as this one, but if higher scale is desired,
the connection should be opened and closed on each request.
That should be done using the __enter__ and __exit__ methods, so that the
caller has control over the connection scope. 
Since we are keeping the connection open as said before, these methods
are non-ops."""


class MySqlRepository(AbstractRepository):

    def __init__(self, host, port, db, user, password, charset, timeout):
        self.conn = MySqlRepository.__create_connection(
            host, port, db, user, password, charset, timeout)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def add(self, prop):
        stmt = 'INSERT INTO properties (internal_id, provider, url) VALUES (%s, %s, %s)'
        with self.conn.cursor() as cursor:
            cursor.execute(
                stmt, (prop['internal_id'], prop['provider'], prop['url']))
            self.conn.commit()

    def get(self, internal_id, provider) -> Property:
        stmt = 'SELECT * FROM properties WHERE internal_id=%s AND provider=%s'
        with self.conn.cursor() as cursor:
            cursor.execute(
                stmt, (internal_id, provider))
            result = cursor.fetchone()

        return result

    @staticmethod
    def initialize_database(host, port, db, user, password, charset, timeout):
        connection = MySqlRepository.__create_connection(
            host, port, db, user, password, charset, timeout)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS properties (
                        id integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
                        internal_id text NOT NULL,
                        provider text NOT NULL,
                        url text NOT NULL,
                        captured_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                    '''
                )
                connection.commit()
            # When indexing a text field in MySQL, it's necessary to specify how many characters to index for each value.
            # In this case, we chose 50, but it could probably be a lot smaller. Since we won't be dealing with massive
            # amounts of data, this is not a concern.
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    CREATE INDEX properties_internal_provider ON properties (internal_id(50), provider(50));
                    '''
                )
                connection.commit()

    @staticmethod
    def __create_connection(host, port, db, user, password, charset, timeout):
        return pymysql.connect(
            charset=charset,
            connect_timeout=timeout,
            cursorclass=pymysql.cursors.DictCursor,
            db=db,
            host=host,
            password=password,
            read_timeout=timeout,
            port=port,
            user=user,
            write_timeout=timeout,
        )
