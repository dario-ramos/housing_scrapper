import telegram
import logging
import numpy as np
import time


class NullNotifier:
    def notify(self, properties):
        pass


class TelegramNotifier(NullNotifier):
    def __init__(self, config):
        logging.info(f"Setting up bot with token {config.notifier_token()}")
        self.config = config
        self.bot = telegram.Bot(token=self.config.notifier_token())

    async def notify(self, properties):
        logging.info(f'Notifying about {len(properties)} properties')
        text = np.random.choice(self.config.notifier_messages())
        async with self.bot:
            await self.bot.send_message(
                chat_id=self.config.notifier_chat_id(), text=text)

        for prop in properties:
            logging.info(f"Notifying about {prop['url']}")

            for i in range(1, self.config.notifier_max_retry()):
                try:
                    async with self.bot:
                        await self.bot.send_message(chat_id=self.config.notifier_chat_id(),
                                          text=f"[{prop['title']}]({prop['url']})",
                                          parse_mode=telegram.constants.ParseMode.MARKDOWN)
                        time.sleep(self.config.notifier_lapse())
                        break
                except telegram.TelegramError as e:
                    self.handle_tg_error(e)

    def notify_error(self, msg):

        for i in range(1, self.config.notifier_max_retry()):
            try:
                self.bot.send_message(chat_id=self.config.notifier_chat_id(),
                                      text=f"<code>{msg}</code>",
                                      parse_mode=telegram.ParseMode.HTML)
                time.sleep(self.config.notifier_lapse())
                break
            except telegram.TelegramError as e:
                self.handle_tg_error(e)

    def handle_tg_error(self, e):
        tg_backoff = 30
        logging.warn(e)
        logging.info(
            f"Hit Telegram rate limit, will sleep for {tg_backoff} seconds and retry")
        time.sleep(tg_backoff)

    @staticmethod
    def get_instance(config):
        if config.notifier_enabled():
            return TelegramNotifier(config)
        else:
            return NullNotifier()
