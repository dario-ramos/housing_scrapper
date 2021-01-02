import html
import logging
import string
import re
from bs4 import BeautifulSoup
from providers.base_provider import BaseProvider


class Bertoia(BaseProvider):
    def props_in_source(self, source):
        page_link = self.provider_data['base_url'] + source

        while True:
            properties, page_content = self.scrape_properties(page_link)
            if len(properties) == 0:
                break

            for prop in properties:
                yield self.scrape_property(prop, source)

            page_link = self.get_next_page_link(page_content)
            if page_link == "":
                break

    def scrape_properties(self, page_link):
        logging.info("Requesting %s" % page_link)
        page_response = self.request(page_link)
        if page_response.status_code != 200:
            logging.error(
                f"Could not retrieve page, got error {page_response.status_code}")
            return [], None

        page_content = BeautifulSoup(page_response.content, 'lxml')
        container = page_content.find('div', id='grid-view')
        if container == None:
            return [], page_content
        return (container.find_all('div', class_='property-item'), page_content)

    def scrape_property(self, prop, source):
        prop_name = prop.find(
            'div', class_='property-name').find('a').get_text()
        location = prop.find('div', class_='property-location')
        raw_title = location.find(
            'div', class_='pull-left').get_text("|", strip=True)
        # Remove non-printable characters
        title = ''.join(s for s in raw_title if s in string.printable)
        # Compact spaces
        title = re.sub(' +', ' ', title)
        # Add space after |
        title = title.replace("|", "| ")
        link = prop.find('div', class_='property-name').find('a')
        internal_id = location.find(
            'div', class_='pull-right').find('span').get_text().strip()

        return {
            'title': prop_name + " | " + title,
            'url': link['href'],
            'internal_id': internal_id,
            'provider': self.provider_name
        }

    def get_next_page_link(self, page_content):
        paginator = page_content.find('div', class_='pagination')
        if paginator == None:
            return ""

        next_button = paginator.find('a', class_='next')
        if next_button == None:
            return ""

        return next_button['href']
