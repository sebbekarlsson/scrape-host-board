from scrapehost.mongo import db
import subprocess
from subprocess import CalledProcessError


def get_active_scrapers():
    return list(
        db.collections.find({
            'structure': '#Scraper',
            'status': 1
        })
    )

def is_service_running(service_name):
    try:
        output = subprocess.check_output(
                [
                    'systemctl',
                    'status',
                    service_name
                    ]
                )
        return '(running)' in str(output)
    except (CalledProcessError, OSError):
        return False

def is_scraping_service_running():
    return is_service_running('scrape.host.scraper.service')


print(is_scraping_service_running())
