from requests import Session
from requests.exceptions import InvalidSchema, MissingSchema, ConnectionError
from bs4 import BeautifulSoup
from scrapehost.mongo import db
import urlparse


class ScraperInstance(object):

    def __init__(self, scraper):
        self.session = Session()
        self.scraper = scraper
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
        return 'import' not in query and 'db.' and 'request' not in query

    def visit_url(self, url):
        try:
            res = self.session.get(url)
        except (InvalidSchema, MissingSchema, ConnectionError):
            return None
        
        if url not in self.visited_urls:
            self.visited_urls.append(url)
        
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
            if self.is_query_ok(self.query):
                try:
                    exec(self.query)
                except:
                    return None

        db.collections.update_one({
            'structure': '#Scraper',
            '_id': self.scraper['_id']
        },
        {
            '$set': {
                'url_index': self.url_index,
                'visited_urls': self.visited_urls,
                'found_urls': self.found_urls,
                'data': self.data
            }
        }
        )

    def tick(self):
        current_url = self.found_urls[self.url_index]

        if self.domain_restrict:
            if not self.location in current_url:
                self.found_urls.pop(self.url_index)
                return None

        self.visit_url(current_url)

        if self.url_index < len(self.found_urls) - 1:
            self.url_index += 1
        else:
            self.url_index = 0
