## About this project

- [About this project](#about-this-project)
- [Configuration](#configuration)
  - [Telegram notifier](#telegram-notifier)
  - [Providers](#providers)
  - [Database](#database)
    - [SQLite](#sqlite)
    - [MySQL](#mysql)
- [Running locally](#running-locally)
- [Running inside a Docker container](#running-inside-a-docker-container)
- [Acceptance tests](#acceptance-tests)

In my pursue of a new place to live, I was tired of having to remember which properties I had already checked, and also having to remember to go to the listings sites.

When I started bookmarking the queries I did in every listing site I realized that what I was doing could be easily automated, and voilà!

Meet housing scraper, an app that queries the listings sites for you and notifies you over Telegram when a new property shows up. It remembers the one it notified you about so you won't receive the same property again.

This initial version is aimed at the Argentinean market, therefore there are only providers that list housing in Argentina.

I'd love to receive comments, bugs, ideas, suggestion (I don't use Python daily, please help me be more pythonic if you'd like to), etc. File an issue in the repo to do so.

## Configuration

There's a `sample.env` file that you can use as a template for your configuration. It also documents the meaning of each configuration key.
Copy that file to a new one in the root folder, name it `.env` and start editing its values.

You need to configure two aspects of the script: the listing providers and the notifier.

### Telegram notifier

For the notifier you need to create a Telegram bot first: [Create a Telegram bot](https://core.telegram.org/bots)

Creating the bot will give you an authorization token. Save it for later, you'll need it.

A bot can't talk with you directly, you have two options: you talk to it first, thus allowing it to reply to you, or you can add it to a group. Whatever option you choose, you need to get the `chat_id` of either your account or the group.

After you've done either of the above, copy and paste the authorization token into the script in `getchatid.py`, and run it. You'll see a JSON blob; look for the Chat object, and get its id field; that's the `chat_id` you need to save for later. Write it down :-)

If `getchatid.py` fails with an index error, you are getting no updates. This can happen because your bot has been inactive for a long time. In the Telegram mobile app, go to Botfather and restart your bot. After a short while, you should be able to get updates and the chat id.

With the authorization token and the chat id you can now configure the notifier. Here's an example (showing only the keys you need to set):

```
NOTIFIER_TOKEN = <TOKEN>
NOTIFIER_CHAT_ID = <CHAT_ID>
```

### Providers

One down, one more to go. Now we need to configure the providers. This is done via key-value pairs in your .env file. To keep this README clean, sample provider configurations are listed [here](docs/providers.md).

### Database

There is only one option now, defined by the DATABASE_STORE key:

- localsqlite: Local SQLite database.

We used to support Heroku, but it's gone. So it will be just local sqlite until we find a new free alternative. Although we will probably just keep a pc on running the sqlite version all day.

#### SQLite

To initialize the database, just run `python3 initsqlitedb.py` and that's it. It will create a sqlite3 db file (by default, named `properties.db`) in the root folder, and the notified listings will be saved there. Simply delete this file and run the script again to reset the database.

#### MySQL

Database initialization should be performed manually in your server. Use this SQL snippet to create the table:

```
CREATE TABLE IF NOT EXISTS properties (
    id integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
    internal_id text NOT NULL,
    provider text NOT NULL,
    url text NOT NULL,
    captured_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Then, fill in the 7 keys in .env that start with the `MYSQL_` prefix. All those values should be obtainable from your server or hosting service.

## Running locally

See detailed guide [here](docs/local.md).

## Running inside a Docker container

See detailed guide [here](docs/docker.md)

## Acceptance tests

These are implemented using gherkin and the behave module. To run them, just enter the command `behave` in the project root directory. These tests create a local sqlite database, which is deleted after the test run. They send their Telegram notifications to a test bot created specifically for testing; you can find its token and a group chat id in `features/steps/scraping.py`, in the function decorated with `@given('we have a test configuration with sqlite store and Telegram notifications')`.

Acceptance tests are meant to run in an environment as close as possible to production; that's why a real database and telegram bot are used. In the future, other kinds of tests should be added to ensure a higher quality.
