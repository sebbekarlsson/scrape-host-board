from requests import Session
from requests.exceptions import InvalidSchema, MissingSchema
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

    def visit_url(self, url):
        try:
            res = self.session.get(url)
        except (InvalidSchema, MissingSchema): #TODO: instead of catching MissingSchema, urljoin
            return None

        self.visited_urls.append(url)
        
        if res.text:
            soup = BeautifulSoup(res.text, 'html.parser')

            for a_tag in soup.find_all('a'):
                href = a_tag.get('href')

                if not href:
                    continue
                
                if 'http' not in href:
                    href = urlparse.urljoin(url, href)

                self.found_urls.append(href)

        db.collections.update_one({
            'structure': '#Scraper',
            '_id': self.scraper['_id']
        },
        {
            '$set': {
                'location': url    
            }
        }
        )

    def tick(self):
        current_url = self.found_urls[self.url_index]

        self.visit_url(current_url)

        if self.url_index < len(self.found_urls) - 1:
            self.url_index += 1
