images = document.find_all('img')


for img in images:
    src = img.get('src')

    if src:
        if 'http' not in src:
            src = urlparse.urljoin(url, src)

        self.data.append(src)
