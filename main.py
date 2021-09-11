#!/usr/bin/env python

from errors.logger_setup import logger
from scraper.config import Config
from scraper.scraper import Scraper

cfg = Config()
scraper = Scraper(cfg)
new_prop_count = scraper.scrape_all()

logger.info(f"Done! Found a total of {new_prop_count} new properties")
