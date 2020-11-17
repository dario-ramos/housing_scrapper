from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import logging

from providers.base_provider import BaseProvider

# Because Remax loads the results dynamically using Ajax, we need to use Selenium
# webdriver to wait for those results to be loaded before trying to parse them
# with BeautifulSoup
class Remax(BaseProvider):
    def props_in_source(self, source):
        page_link = self.provider_data['base_url'] + source
        page = 1
        driverOptions = Options()
        driverOptions.headless = True
        driver = webdriver.Chrome(options=driverOptions, executable_path=self.provider_data['chromedriver'])
        delay = 3 # Seconds
        pageCount = None

        while True:
            logging.info(f"Requesting {page_link}")
            driver.get(page_link)
            try:
                _ = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'gallery-item-container')))
            except TimeoutException:
                logging.info("Timed out waiting for properties data")
                break

            page_content = BeautifulSoup(driver.page_source, 'lxml')
            properties = page_content.find_all('div', class_='gallery-item-container')

            if pageCount == None:
                pageCount = getPageCount(page_content)

            if len(properties) == 0:
                break
            else:
                logging.info("Found %d properties to scrape", len(properties))

            for prop in properties:
                link = prop.find('div', class_='gallery-photo').find('a')
                href = link['href']

                title = link.get_text().strip()
                price_section = prop.find('div', class_='gallery-price')
                if price_section is not None:
                    title = title + ' ' + price_section.get_text().strip()

                internal_id = prop['id']
                yield {
                    'title': title, 
                    'url': self.provider_data['base_url'] + href,
                    'internal_id': internal_id,
                    'provider': self.provider_name
                    }

            page += 1
            # page_link = self.provider_data['base_url'] + source.replace(".html", f"-pagina-{page}.html")
            break

    def getPageCount(page_content):
        page_content.find_all('div', class_='')