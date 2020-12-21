from .sqliterepository import SqliteRepository
from .herokupgrepository import HerokuPgRepository, getDbUriFromHeroku


def get_factory(cfg):
    def create_sql_lite_repository():
        return SqliteRepository('properties.db')

    def create_herokupg_repository(conn_info):
        return HerokuPgRepository(conn_info)

    if cfg['store'] == 'localsqlite':
        return create_sql_lite_repository
    elif cfg['store'] == 'herokupg':
        conn_uri = getDbUriFromHeroku(cfg['heroku_app_name'])
        return create_herokupg_repository(conn_uri)

    else:
        raise LookupError(
            f"Invalid store {cfg['store']}. Supported values: localsqlite,herokupg")
