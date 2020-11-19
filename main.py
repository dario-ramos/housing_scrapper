#!/usr/bin/env python

import logging
import yaml
import sys
import traceback
from notifier import Notifier
from providers.processor import process_properties

# logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# configuration
with open("configuration.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

notifier = Notifier.get_instance(cfg['notifier'])

new_properties = []
for provider_name, provider_data in cfg['providers'].items():
    try:
        logging.info(f"Processing provider {provider_name}")
        new_properties += process_properties(provider_name, provider_data)
        if len(new_properties) > 0:
            notifier.notify(new_properties)
            logging.info(
                f"Done! Found {len(new_properties)} new properties :)")
        else:
            logging.info("No new properties found :(")
    except Exception as e:
        logging.error(
            f"Error processing provider {provider_name}.\n{sys.exc_info()[0]}")
        print(''.join(traceback.format_exception(None, e, e.__traceback__)))
