from .sqliterepository import SqliteRepository


def get_factory(cfg):
    def create_sql_lite_repository():
        return SqliteRepository('properties.db')

    if cfg['store'] == 'localsqlite':
        return create_sql_lite_repository
    else:
        raise LookupError(
            f"Invalid store {cfg['store']}. Supported values: localsqlite")

    return create_sql_lite_repository
