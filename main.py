#!/usr/bin/env python

import logging
import sys
import traceback
from notifier import Notifier

from providers.processor import process_properties
from database.repositoryfactory import get_factory
from errors.factory import create_error_handler
from config import Config

# logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# configuration
cfg = Config()

notifier = Notifier.get_instance(cfg)
repository_factory = get_factory(cfg)
error_handler = create_error_handler(cfg.error_handler(), notifier)

new_prop_count = 0
for provider_name, provider_data in cfg.providers().items():
    try:
        logging.info(f"Processing provider {provider_name}")
        new_properties = process_properties(
            provider_name, provider_data, repository_factory)
        if len(new_properties) > 0:
            logging.info(
                f"Found {len(new_properties)} new properties for provider {provider_name} :)")
            notifier.notify(new_properties)
            new_prop_count += len(new_properties)
        else:
            logging.info(
                f"No new properties found for provider {provider_name} :(")
    except Exception as e:
        error_handler.handle_exception(f"Error in provider {provider_name}", e)

logging.info(f"Done! Found a total of {new_prop_count} new properties")
