from scrapehost.scraping.utils import get_active_scrapers



class ScraperService(object):

    def __init__(self):
        self.scrapers = []
    
    def tick(self):
        self.scrapers = get_active_scrapers()

        for scraper in self.scrapers:
            scraper.tick()
