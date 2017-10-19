from scrapehost.scraping.utils import get_active_scrapers



class ScraperService(object):

    def __init__(self):
        self.scrapers = []
        self.scrapers = get_active_scrapers()
    
    def tick(self):
        for scraper in self.scrapers:
            scraper.tick()
