from scrapehost.scraping.ScraperService import ScraperService


if __name__ == '__main__':
    service = ScraperService()
    
    # game loop thinkstyle
    try:
        while True:
            service.tick()
    except KeyboardInterrupt:
        print('Exiting...')
        quit()
