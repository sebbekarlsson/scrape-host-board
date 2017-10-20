from scrapehost.scraping.ScraperService import ScraperService


if __name__ == '__main__':
    service = ScraperService()
    
    print('Starting scraping service...')
    try:
        while True:
            service.tick()
    except KeyboardInterrupt:
        print('Exiting...')
        quit()
