from behave import fixture
from database.sqliterepository import SqliteRepository
import os


@fixture
def before_scenario(context, scenario):
    SqliteRepository.initialize_database('test.db')


def after_scenario(context, scenario):
    os.remove('test.db')
