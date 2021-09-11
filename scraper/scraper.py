from database.repositoryfactory import get_factory
from errors.factory import create_error_handler
from errors.logger_setup import logger
from notifications.telegram_notifier import TelegramNotifier
from providers.factory import get_instance


class Scraper:

    def __init__(self, cfg):
        self.cfg = cfg
        self.notifier = TelegramNotifier.get_instance(cfg)
        self.repository_factory = get_factory(cfg)
        self.error_handler = create_error_handler(
            cfg.error_handler(), self.notifier)

    def scrape_all(self):

        new_prop_count = 0
        for provider_name, provider_data in self.cfg.providers().items():
            try:
                logger.info(f"Processing provider {provider_name}")
                new_properties = self.scrape_one(
                    provider_name, provider_data, self.repository_factory)
                if len(new_properties) > 0:
                    logger.info(
                        f"Found {len(new_properties)} new properties for provider {provider_name} :)")
                    self.notifier.notify(new_properties)
                    new_prop_count += len(new_properties)
                else:
                    logger.info(
                        f"No new properties found for provider {provider_name} :(")
            except Exception as e:
                self.error_handler.handle_exception(
                    f"Error in provider {provider_name}", e)
        return new_prop_count

    def scrape_one(self, provider_name, provider_data, repository_factory):
        provider = get_instance(provider_name, provider_data)

        new_properties = []

        with repository_factory() as repo:
            for prop in provider.next_prop():
                result = repo.get(prop['internal_id'], prop['provider'])
                if result == None:
                    # Insert and save for notification
                    logger.info('It is a new one')
                    repo.add(prop)
                    new_properties.append(prop)

        return new_properties
