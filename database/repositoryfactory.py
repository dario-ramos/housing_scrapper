from .sqliterepository import SqliteRepository

def get_factory(cfg):
    def create_sql_lite_repository():
        return SqliteRepository(cfg.local_sqlite_file())

    store = cfg.database_store()
    if store == 'localsqlite':
        return create_sql_lite_repository
    else:
        raise LookupError(
            f"Invalid store {store}. Supported values: localsqlite")
