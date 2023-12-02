#!/usr/bin/env python

import asyncio
from errors.logger_setup import logger
from scraper.config import Config
from scraper.scraper import Scraper

async def main():
    cfg = Config()
    scraper = Scraper(cfg)
    new_prop_count = await scraper.scrape_all()

    logger.info(f"Done! Found a total of {new_prop_count} new properties")

if __name__ == '__main__':
    asyncio.run(main())
