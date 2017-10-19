from scrapehost.scraping.utils import get_active_scrapers



class ScraperService(object):

    def __init__(self):
        self.scrapers = []

    def initialize(self):
        self.scrapers = get_active_scrapers()

    def tick(self):
        self.initialize()

        for scraper in self.scrapers:
            scraper.tick()
