from .sqliterepository import SqliteRepository
from .herokupgrepository import HerokuPgRepository, getDbUriFromHeroku


def get_factory(cfg):
    def create_sql_lite_repository():
        return SqliteRepository('properties.db')

    def create_herokupg_repository(conn_info):
        return HerokuPgRepository(conn_info)

    store = cfg.database_store()
    if store == 'localsqlite':
        return create_sql_lite_repository
    elif store == 'herokupg':
        conn_uri = getDbUriFromHeroku(cfg.heroku_app_name())
        return create_herokupg_repository(conn_uri)

    else:
        raise LookupError(
            f"Invalid store {store}. Supported values: localsqlite, herokupg")
