#!/usr/bin/env python

import telegram
import logging
import numpy as np
import time


class NullNotifier:
    def notify(self, properties):
        pass


class Notifier(NullNotifier):
    def __init__(self, config):
        logging.info(f"Setting up bot with token {config.notifier_token()}")
        self.config = config
        self.bot = telegram.Bot(token=self.config.notifier_token())

    def notify(self, properties):
        logging.info(f'Notifying about {len(properties)} properties')
        text = np.random.choice(self.config.notifier_messages())
        self.bot.send_message(
            chat_id=self.config.notifier_chat_id(), text=text)

        for prop in properties:
            logging.info(f"Notifying about {prop['url']}")

            while True:
                try:
                    self.bot.send_message(chat_id=self.config.notifier_chat_id(),
                                          text=f"[{prop['title']}]({prop['url']})",
                                          parse_mode=telegram.ParseMode.MARKDOWN)
                    # TODO Make this configurable
                    time.sleep(10)
                    break
                except telegram.TelegramError as e:
                    logging.warn(e)
                    logging.info(
                        "Hit Telegram rate limit, will sleep for 30 seconds and retry")
                    # TODO Make this configurable
                    time.sleep(30)

    @staticmethod
    def get_instance(config):
        if config.notifier_enabled():
            return Notifier(config)
        else:
            return NullNotifier()
