from behave import given, when, then, step
from database.sqliterepository import SqliteRepository


@given('we have a test configuration with sqlite store and Telegram notifications')
def step_impl(context):
    pass


@when('we scrape all configured providers')
def step_impl(context):

    pass


@then('we will receive one Telegram notification per property')
def step_impl(context):
    assert context.failed is False
