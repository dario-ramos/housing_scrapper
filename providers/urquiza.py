import logging
from bs4 import BeautifulSoup
from providers.base_provider import BaseProvider
from providers.urlhelper import set_query_param


class Urquiza(BaseProvider):
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
                page_link = set_query_param(page_link, 'pagina', page)

    def scrape_properties(self, page_link):
        logging.info("Requesting %s" % page_link)
        page_response = self.request(page_link)
        if page_response.status_code != 200:
            logging.error(
                f"Could not retrieve page, got error {page_response.status_code}")
            return [], None

        page_content = BeautifulSoup(page_response.content, 'lxml')
        paginator_text = page_content.find(
            'ul', class_='pagination').get_text().strip()
        if paginator_text == "No se encontraron propiedades":
            return [], page_content
        return (page_content.find_all('div', class_='ResultadoCaja'), page_content)

    def get_page_count(self, page_content):
        paginator = page_content.find('ul', class_='pagination')
        pages = paginator.find_all('li')

        page_count = 0
        for page in pages:
            if page.get_text().isnumeric():
                page_count += 1
        return page_count

    def scrape_property(self, prop, source):
        link = prop.find('div', class_='resultadoTipo').find('a')
        title = link.get_text() + ' | ' + prop.find('div',
                                                    class_='resultadoLocalidad').get_text()

        price = prop.find('div', class_='resultadoPrecio')
        if price != None:
            title += ' | ' + price.get_text()

        internal_id = prop.find('div', class_='codigo').get_text()

        return {
            'title': title,
            'url': link['href'],
            'internal_id': internal_id,
            'provider': self.provider_name
        }
