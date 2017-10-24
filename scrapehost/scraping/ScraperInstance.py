# -*- coding: utf-8 -*-
from requests import Session
from requests.exceptions import (
    InvalidSchema,
    MissingSchema,
    ConnectionError,
    SSLError
)
from bs4 import BeautifulSoup
from scrapehost.mongo import db
import urlparse
from scrapehost.scraping.robotstxt import RobotsTXTParser
import os


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
        self.robotstxt = RobotsTXTParser()
        self.error = scraper['error']
        self.blocked_extensions = [
            '.m4a',
            '.m4v',
            '.zip',
            '.tar.gz',
            '.mov',
            '.rar',
            '.pdf'
        ]

        if not self.data:
            self.data = []

        if len(self.found_urls) == 0:
            self.found_urls.append(self.location)

    def is_query_ok(self, query):
        return 'import' not in query and 'db.' not in query\
                and 'request' not in query and 'open(' not in query\
                and 'with ' not in query and query.count('\n') < 25

    def visit_url(self, url, collect_data):
        parsed_url = urlparse.urlparse(url)
        ext = os.path.splitext(parsed_url.path)[1].lower()

        if collect_data and ext not in self.blocked_extensions:
            all_ok = True
            
            self.robotstxt.set_robots_url('{}://{}/robots.txt'.format(
                parsed_url.scheme,
                parsed_url.netloc
            ))

            if self.robotstxt.is_allowed(parsed_url.path):
                try:
                    print('{} is visiting: {}'.format(self.name, url))
                except:
                    print('...')

                print('robots.txt says it is okay!')

                try:
                    res = self.session.get(url)
                except (InvalidSchema, MissingSchema, ConnectionError):
                    self.found_urls.pop(self.url_index)
                    all_ok = False
            else:
                self.found_urls.pop(self.url_index)
                all_ok = False

            if all_ok:
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
                            except Exception as e:
                                self.error = str(e)
                            else:
                                self.error = None
        else:
            self.found_urls.pop(self.url_index)

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
                'data': self.data,
                'error': self.error
            }
        }
        )

    def tick(self):
        try:
            current_url = self.found_urls[self.url_index]
        except IndexError:
            current_url = self.found_urls[0]

        collect_data = True

        if self.domain_restrict:
            p_uri_0 = urlparse.urlparse(self.location).netloc.replace('www.', '')
            p_uri_1 = urlparse.urlparse(current_url).netloc.replace('www.', '')

            if p_uri_0 not in p_uri_1:
                print('Will pop: {}'.format(current_url))
                self.found_urls.pop(self.url_index)
                collect_data = False
        
        self.visit_url(current_url, collect_data)
