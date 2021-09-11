from .sqliterepository import SqliteRepository
from .herokupgrepository import HerokuPgRepository, getDbUriFromHeroku


def get_factory(cfg):
    def create_sql_lite_repository():
        return SqliteRepository(cfg.local_sqlite_file())

    def create_herokupg_repository():
        conn_uri = getDbUriFromHeroku(cfg.heroku_app_name())
        return HerokuPgRepository(conn_uri)

    store = cfg.database_store()
    if store == 'localsqlite':
        return create_sql_lite_repository
    elif store == 'herokupg':
        return create_herokupg_repository

    else:
        raise LookupError(
            f"Invalid store {store}. Supported values: localsqlite, herokupg")
