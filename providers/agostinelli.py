import logging
from bs4 import BeautifulSoup
from providers.base_provider import BaseProvider


class Agostinelli(BaseProvider):
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
        return (page_content.find_all('div', class_='sm-result-wrapper'), page_content)

    def scrape_property(self, prop, source):
        operation = prop.find('div', class_='operation')
        property_type = operation.find('span').get_text()
        address = prop.find('h6').get_text()
        title = ''.join([operation.get_text(), prop], ' | ')
