from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import logging
import re
from providers.base_provider import BaseProvider


class Mercadolibre(BaseProvider):
    def props_in_source(self, source):
        page_link = self.provider_data['base_url'] + source + '_NoIndex_True'
        page = 1
        page_count = None
        regex = r"(MLA-\d*)"
        driver_options = Options()
        driver_options.headless = True
        driver = webdriver.Chrome(options=driver_options)
        timeout = self.provider_data['timeout']

        while(True):
            properties, page_content = self.scrape_properties(
                page_link, driver, timeout)

            if len(properties) == 0:
                break

            if page_count == None:
                page_count = self.get_page_count(page_content)

            for prop in properties:
                yield self.scrape_property(prop, regex)

            page += 1
            if page > page_count:
                break
            else:
                page_link = self.get_next_page_link(page_content, page)

    def scrape_properties(self, page_link, driver, timeout):
        logging.info(f"Requesting {page_link}")

        driver.get(page_link)
        try:
            _ = WebDriverWait(driver, timeout).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, 'ui-search-layout__item')))
        except TimeoutException:
            logging.warn('Timed out waiting for results')
            return ([], None)

        page_content = BeautifulSoup(driver.page_source, 'lxml')
        return (page_content.find_all('li', class_='ui-search-layout__item'), page_content)

    def get_page_count(self, page_content):
        paginator = page_content.find('ul', class_='ui-search-pagination')
        if paginator == None:
            return 1

        pages = paginator.find_all('li')

        page_count = 0
        for page in pages:
            if page.find('a').get_text().isnumeric():
                page_count += 1
        return page_count

    def get_next_page_link(self, page_content, next_page_number):
        paginator = page_content.find('ul', class_='ui-search-pagination')
        pages = paginator.find_all('li')

        for page in pages:
            page_number = page.find('a').get_text().strip()
            if page_number.isnumeric() and page_number == str(next_page_number):
                return page.find('a')['href']

        return ''

    def scrape_property(self, prop, regex):
        section = prop.find('a', class_='ui-search-result__link')
        if section is None:
            section = prop.find(
                'a', class_='ui-search-result__content')
        href = section['href']
        matches = re.search(regex, href)
        internal_id = matches.group(1).replace('-', '')
        price_section = section.find('span', class_='price-tag')
        title_section = section.find(
            'div', class_='ui-search-item__group--title')
        title = title_section.find('span').get_text().strip() + \
            ': ' + title_section.find('h2').get_text().strip()
        if price_section is not None:
            title = title + ' ' + price_section.get_text().strip()

        return {
            'title': title,
            'url': href,
            'internal_id': internal_id,
            'provider': self.provider_name
        }
