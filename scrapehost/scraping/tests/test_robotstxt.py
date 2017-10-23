from scrapehost.scraping.robotstxt import RobotsTXTParser


robots_txt_content = """
User-agent: bingbot
Crawl-delay: 5
Disallow: /aspnet_client/
Disallow: /bin/
Disallow: /ClientBin/
Disallow: /config/
Disallow: /css/
Disallow: /data/
Disallow: /install/
Disallow: /scripts/
Disallow: /umbraco/
Disallow: /umbraco_client/
Disallow: /usercontrols/
Disallow: /xslt/
Disallow: /search/
Disallow: /raw/
Disallow: /soa/
Disallow: /services/
Disallow: /base/
Disallow: /error/
Disallow: /staged-content/
Disallow: /authors/
Disallow: /admin/
"""


def test_disallowed_path():
    parser = RobotsTXTParser()
    parser.set_robots_content(robots_txt_content)

    assert parser.is_allowed('/ClientBin') == False
    assert parser.is_allowed('/ClientBin/not-ok') == False
    assert parser.is_allowed('/ClientBin/not-ok/hello') == False

def test_allowed_path():
    parser = RobotsTXTParser()
    parser.set_robots_content(robots_txt_content)

    assert parser.is_allowed('/this-path-is-allowed/ok') == True 
    assert parser.is_allowed('/this-path-is-allowed/123/hello-world') == True
    assert parser.is_allowed('/this-path-is-allowed/hello/test') == True

def test_crawl_delay():
    parser = RobotsTXTParser()
    parser.set_robots_content(robots_txt_content)
    
    return parser.get_crawl_delay() == 5
