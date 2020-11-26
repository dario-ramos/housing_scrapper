#import requests
from bs4 import BeautifulSoup
import logging
from providers.base_provider import BaseProvider


class Zonaprop(BaseProvider):
    def props_in_source(self, source):
        page_link = self.provider_data['base_url'] + source
        page = 1
        page_count = None

        while(True):
            properties, page_content = self.scrape_properties(page_link)

            if len(properties) == 0:
                break

            for prop in properties:
                yield self.scrape_property(prop)

            if page_count == None:
                page_count = self.get_page_count(page_content)
            page += 1
            if page > page_count:
                break
            else:
                page_link = self.get_next_page_link(source, page)

    def scrape_properties(self, page_link):
        logging.info(f"Requesting {page_link}")
        page_response = self.request(page_link)

        if page_response.status_code != 200:
            logging.warn(
                f"Page request failed with code {page_response.status_code}")
            return [], None

        page_content = BeautifulSoup(page_response.content, 'lxml')
        return (page_content.find_all('div', class_='postingCard'), page_content)

    def scrape_property(self, prop):
        title = prop.find(
            'a', class_='go-to-posting').get_text().strip()
        price_section = prop.find('span', class_='first-price')
        if price_section is not None:
            title = title + ' ' + price_section['data-price']

        return {
            'title': title,
            'url': self.provider_data['base_url'] + prop['data-to-posting'],
            'internal_id': prop['data-id'],
            'provider': self.provider_name
        }

    def get_page_count(self, page_content):
        paginator = page_content.find('div', id='react-paging')
        if paginator == None:
            return 1

        pages = paginator.find_all('li')
        if pages == None or len(pages) == 0:
            return 1

        page_count = 0
        for page in pages:
            if page.find('a').get_text().strip().isnumeric():
                page_count += 1

        return page_count

    def get_next_page_link(self, source, page):
        return self.provider_data['base_url'] + source.replace('.html', '') + f"-pagina-{page}" + '.html'
