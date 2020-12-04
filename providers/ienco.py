import logging
import re
from bs4 import BeautifulSoup
from providers.base_provider import BaseProvider


class Ienco(BaseProvider):
    def props_in_source(self, source):
        page_link = self.provider_data['base_url'] + source
        page = 1
        pageCount = None

        while True:
            properties, page_content = self.scrape_properties(page_link)
            if len(properties) == 0:
                break

            if pageCount == None:
                pageCount = self.get_page_count(page_content)

            for prop in properties:
                yield self.scrape_property(prop, source)

            page += 1
            if page > pageCount:
                break
            else:
                page_link = self.get_next_page_link(page_content, page)

    def scrape_properties(self, page_link):
        logging.info("Requesting %s" % page_link)
        page_response = self.request(page_link)
        if page_response.status_code != 200:
            logging.error(
                f"Could not retrieve page, got error {page_response.status_code}")
            return [], None

        page_content = BeautifulSoup(page_response.content, 'lxml')
        return (page_content.find_all('div', class_='item-listing-wrap card'), page_content)

    def get_page_count(self, page_content):
        paginator = page_content.find('ul', class_='pagination')
        if paginator == None:
            return 1

        pages = paginator.find_all('a')
        # If the last two are non-numeric, there are more than 3 pages
        # and the last one's link contains the page count
        if len(pages) >= 2:
            last = pages[-1].get_text().strip()
            before_last = pages[-2].get_text().strip()
            if not last.isnumeric() and not before_last.isnumeric():
                match = re.search(r'/page/(\d)', pages[-1]['href'])
                return int(match.group(1))

        page_count = 0
        for p in pages:
            if p.get_text().isnumeric():
                page_count += 1
        return page_count

    def scrape_property(self, prop, source):
        card_title = prop.find('h2', class_='item-title')
        title = card_title.get_text().replace('\n', '')
        address = prop.find('address', class_='item-address')
        if address != None:
            title += ' | ' + address.get_text()
        price = prop.find('li', class_='item-price')
        if price != None:
            title += ' | ' + price.get_text()

        link = card_title.find('a')

        internal_id = prop['id']

        return {
            'title': title,
            'url': link['href'],
            'internal_id': internal_id,
            'provider': self.provider_name
        }

    def get_next_page_link(self, page_content, next_page_number):
        pages = page_content.find('ul', class_='pagination').find_all('a')

        for p in pages:
            page_number = p.get_text().strip()
            if page_number.isnumeric() and page_number == str(next_page_number):
                return p['href']
        return ''
