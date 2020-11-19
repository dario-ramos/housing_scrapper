import hashlib
import logging
import urllib.parse as urlparse
from bs4 import BeautifulSoup
from providers.base_provider import BaseProvider


class Rogliano(BaseProvider):
    def props_in_source(self, source):
        page_link = self.provider_data['base_url'] + source
        page = 1

        while True:
            if page > 1:
                break

            properties = self.scrape_properties(page_link)
            if len(properties) == 0:
                break

            for prop in properties:
                yield self.scrape_property(prop, source)

            page += 1

    def scrape_properties(self, page_link):
        logging.info("Requesting %s" % page_link)
        page_response = self.request(page_link)
        if page_response.status_code != 200:
            logging.error(
                f"Could not retrieve page, got error {page_response.status_code}")
            return []

        page_content = BeautifulSoup(page_response.content, 'lxml')
        return page_content.find_all('div', class_='modulo_listado_propiedades')

    def scrape_property(self, prop, source):
        link = self.provider_data['base_url'] + source
        internal_id = 'unknown_' + \
            hashlib.sha256(str(prop).encode('utf-8')).hexdigest()
        btn_consultar = prop.find('a', class_='btn_consultar3')
        if btn_consultar != None:
            link = self.provider_data['base_url'] + '/' + btn_consultar['href']
            internal_id = urlparse.parse_qs(urlparse.urlparse(link).query)[
                'id_propiedad'][0]

        title = prop.find('div', class_='col2').find('h3').get_text()

        return {
            'title': title,
            'url': link,
            'internal_id': internal_id,
            'provider': self.provider_name
        }
