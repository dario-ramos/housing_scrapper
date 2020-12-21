from bs4 import BeautifulSoup
from providers.base_provider import BaseProvider
from providers.urlhelper import set_query_param
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from .chromedriverhelper import get_chrome_driver_options
import chromedriver_binary
import logging
import os
import re


class Bonifacio(BaseProvider):
    def props_in_source(self, source):
        page_link = self.provider_data['base_url'] + source
        page = 1
        page_count = None
        driver_options = get_chrome_driver_options()
        driver = webdriver.Chrome(options=driver_options)
        timeout = self.provider_data['timeout']

        while True:
            properties, page_content = self.scrape_properties(
                page_link, driver, timeout)
            if len(properties) == 0:
                break

            if page_count == None:
                page_count = self.get_page_count(page_content)

            for prop in properties:
                yield self.scrape_property(prop, source)

            page += 1
            if page > page_count:
                break
            else:
                page_link = set_query_param(page_link, 'page', page, False)

    def scrape_properties(self, page_link, driver, timeout):
        logging.info("Requesting %s" % page_link)
        driver.get(page_link)
        try:
            _ = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'app-buscador')))
        except TimeoutException:
            logging.warn('Timed out waiting for results')
            return [], None

        page_content = BeautifulSoup(driver.page_source, 'lxml')
        results = page_content.find_all('mat-card', class_='mat-card')

        return (results, page_content)

    def get_page_count(self, page_content):
        paginator = page_content.find('app-pagination')
        pages = paginator.find_all('li')
        return len(pages)-2

    def scrape_property(self, prop, source):
        header = prop.find('div', class_='mat-card-header-text')
        title_div = header.find('mat-card-title', class_='mat-card-title')
        subtitle_div = header.find(
            'mat-card-subtitle', class_='mat-card-subtitle')
        details = prop.find_all('div', class_='mat-list-item-content')

        title = title_div.get_text() + ' ' + subtitle_div.get_text() + \
            ' | ' + details[0].get_text().replace('location_on', '').strip()

        price = re.sub('[^0-9]', '', details[2].get_text())
        if price.isnumeric():
            title += ' | ' + price

        link = prop.find('div', class_='mat-card-image').find('a')

        internal_id = prop.find(
            'app-fav').find('span').get_text().replace('Código', '').strip()

        return {
            'title': title,
            'url': self.provider_data['base_url'] + link['href'],
            'internal_id': internal_id,
            'provider': self.provider_name
        }
