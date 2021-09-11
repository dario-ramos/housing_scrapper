from behave import given, when, then, step
import os
from scraper.config import Config
from scraper.scraper import Scraper


@given('we have a test configuration with sqlite store and Telegram notifications')
def step_impl(context):
    os.environ['NOTIFIER_ENABLED'] = '1'
    os.environ['NOTIFIER_TOKEN'] = '1958942562:AAGKDfy2S7vcXj3cFe0I1-0Hevq8ayM-9U0'
    os.environ['NOTIFIER_MESSAGE'] = 'This is a test notification'
    os.environ['NOTIFIER_CHAT_ID'] = '-545020496'
    os.environ['NOTIFIER_LAPSE'] = '10'
    os.environ['NOTIFIER_MAX_RETRY'] = '5'

    os.environ['DATABASE_STORE'] = 'localsqlite'
    os.environ['LOCAL_SQLITE_FILE'] = 'test.db'
    os.environ['ERROR_HANDLER'] = 'stdout'

    os.environ['PROVIDER1_NAME'] = 'argenprop'
    os.environ['PROVIDER1_ENABLED'] = '1'
    os.environ['PROVIDER1_BASE_URL'] = 'https://www.argenprop.com'
    os.environ['PROVIDER1_S1'] = '/departamento-alquiler-barrio-palermo-2-dormitorios-5-o-más-ambientes'
    context.scraper = Scraper(Config("bogus.env"))


@when('we scrape all configured providers')
def step_impl(context):
    context.property_count = context.scraper.scrape_all()


@then('we will receive one Telegram notification per property in the database')
def step_impl(context):
    assert context.failed is False
    assert context.property_count > 0
