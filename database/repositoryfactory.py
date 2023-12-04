from .sqliterepository import SqliteRepository
from .mysqlrepository import MySqlRepository


def get_factory(cfg):
    def create_sql_lite_repository():
        return SqliteRepository(cfg.local_sqlite_file())

    def create_mysql_repository():
        return MySqlRepository(
            host=cfg.mysql_host(),
            port=cfg.mysql_port(),
            db=cfg.mysql_db(),
            user=cfg.mysql_user(),
            password=cfg.mysql_password(),
            charset=cfg.mysql_charset(),
            timeout=cfg.mysql_timeout()
        )

    store = cfg.database_store()
    if store == 'localsqlite':
        return create_sql_lite_repository
    elif store == 'mysql':
        return create_mysql_repository
    else:
        raise LookupError(
            f"Invalid store {store}. Supported values: localsqlite")
