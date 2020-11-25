from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import logging
from providers.urlhelper import set_query_param

from providers.base_provider import BaseProvider

# Because Remax loads the results dynamically using Ajax, we need to use Selenium
# webdriver to wait for those results to be loaded before trying to parse them
# with BeautifulSoup


class Remax(BaseProvider):
    def props_in_source(self, source):
        page_link = self.provider_data['base_url'] + source
        page = 1
        driver_options = Options()
        driver_options.headless = True
        driver = webdriver.Chrome(
            options=driver_options, executable_path=self.provider_data['chromedriver'])
        timeout = self.provider_data['timeout']
        page_count = None

        while True:
            properties, page_content = self.scrape_properties(
                page_link, driver, timeout)
            if len(properties) == 0:
                break

            if page_count == None:
                page_count = self.getPageCount(page_content)

            for prop in properties:
                yield self.scrape_property(prop)

            page += 1
            if page > page_count:
                break
            else:
                page_link = set_query_param(page_link, 'CurrentPage', page)

    def scrape_properties(self, page_link, driver, timeout):
        logging.info(f"Requesting {page_link}")
        driver.get(page_link)
        try:
            _ = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'gallery-item-container')))
        except TimeoutException:
            page_content = BeautifulSoup(driver.page_source, 'lxml')
            no_listings = page_content.find_all(
                'div', class_='no-listings')
            if no_listings == None:
                logging.info("Timed out waiting for properties data")
            else:
                logging.info("No properties found for this source")
            return [], page_content

        page_content = BeautifulSoup(driver.page_source, 'lxml')
        return (page_content.find_all('div', class_='gallery-item-container'), page_content)

    def getPageCount(self, page_content):
        paginator = page_content.find('ul', class_='pagination')
        if paginator == None:
            return 1
        paginatorItems = paginator.find_all('li')
        return len(paginatorItems)-2

    def scrape_property(self, prop):
        link = prop.find('div', class_='gallery-photo').find('a')
        href = link['href']

        title = link.get_text().strip()
        price_section = prop.find('div', class_='gallery-price')
        if price_section is not None:
            title = title + ' ' + price_section.get_text().strip()

        internal_id = prop['id']
        return {
            'title': title,
            'url': self.provider_data['base_url'] + href,
            'internal_id': internal_id,
            'provider': self.provider_name
        }
