# -*- coding: utf-8 -*-
import requests
import urlparse
from requests.exceptions import (
    SSLError
)


class RobotsTXTParser(object):

    def __init__(self):
        self.robots_url = None
        self.robots_content = None
        self.disallows = []

    def clean_str(self, txt):
        return txt.lower().\
                replace('\n', '').\
                replace('\r', '').\
                replace('/', '').\
                replace(' ', '')

    def get_crawl_delay(self):
        if not self.robots_content:
            return None

        if 'Crawl-delay' not in self.robots_content:
            return None

        crawl_delay = self.robots_content.lower().\
                split('crawl-delay')[1].split('\n')[0].\
                split(':')[1].replace(' ', '')

        return int(crawl_delay)

    def set_robots_url(self, url):
        self.robots_url = url
        
        try:
            res = requests.get(url)
        except SSLError:
            return False

        if res.status_code != 200:
            return False
        
        if res.text:
            self.set_robots_content(res.text)
            
            return True

        return False

    def set_robots_content(self, content):
        self.robots_content = content

        _disallows = self.robots_content.split('Disallow:')
        self.disallows = [dis.split('\n')[0].replace('\r', '') for dis in _disallows]

        return True

    def is_allowed(self, endpoint):
        if len(self.disallows) == 0 or self.robots_content == None:
            return True

        if endpoint.count('/') <= 1:
            return self.clean_str(endpoint) not in [
                self.clean_str(endp) for endp in self.disallows
            ]

        subs = endpoint.split('/')

        for dis in self.disallows:
            if dis == '':
                continue
            
            if self.clean_str(subs[1]) == self.clean_str(dis):
                return False

        return True
