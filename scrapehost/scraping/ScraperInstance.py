from requests import Session
from requests.exceptions import InvalidSchema, MissingSchema, ConnectionError
from bs4 import BeautifulSoup
from scrapehost.mongo import db
import urlparse


class ScraperInstance(object):

    def __init__(self, scraper):
        self.session = Session()
        self.scraper = scraper
        self.name = scraper['name']
        self.visited_urls = scraper['visited_urls']
        self.found_urls = scraper['found_urls']
        self.url_index = int(scraper['url_index'])
        self.domain_restrict = scraper['domain_restrict']
        self.location = scraper['location']
        self.query = scraper['query']
        self.data = scraper['data']

        if not self.data:
            self.data = []

        if len(self.found_urls) == 0:
            self.found_urls.append(self.location)

    def is_query_ok(self, query):
        return 'import' not in query and 'db.' and 'request' not in query\
                and query.count('\n') < 25

    def visit_url(self, url, collect_data):
        if collect_data:
            print('{} is visiting: {}'.format(self.name, url))

            try:
                res = self.session.get(url)
            except (InvalidSchema, MissingSchema, ConnectionError):
                return None

            if res.text:
                soup = BeautifulSoup(res.text, 'html.parser')

                for a_tag in soup.find_all('a'):
                    href = a_tag.get('href')

                    if not href:
                        continue
                    
                    if 'http' not in href:
                        href = urlparse.urljoin(url, href)
                    
                    if href not in self.found_urls:
                        self.found_urls.append(href)
                
                # perform user query
                document = soup
                if self.query:
                    if self.is_query_ok(self.query):
                        try:
                            print('Executing user query...')
                            exec(self.query)
                        except:
                            return None

        if self.url_index < len(self.found_urls) - 1:
            self.url_index += 1
        else:
            self.url_index = 0

        print('Updating scraper...')
        db.collections.update_one({
            'structure': '#Scraper',
            '_id': self.scraper['_id']
        },
        {
            '$set': {
                'url_index': int(self.url_index) + 1,
                'found_urls': self.found_urls,
                'data': self.data
            }
        }
        )

    def tick(self):
        current_url = self.found_urls[self.url_index]
        collect_data = True

        if self.domain_restrict:
            p_uri_0 = urlparse.urlparse(self.location).netloc.replace('www.', '')
            p_uri_1 = urlparse.urlparse(current_url).netloc.replace('www.', '')

            if p_uri_0 not in p_uri_1:
                print('Will pop: {}'.format(current_url))
                self.found_urls.pop(self.url_index)
                collect_data = False
        
        self.visit_url(current_url, collect_data)
