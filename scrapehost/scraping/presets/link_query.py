images = document.find_all('a')


for link in links:
    href = link.get('href')

    if href:
        if 'http' not in href:
            href = urlparse.urljoin(url, href)

        self.data.append(href)
