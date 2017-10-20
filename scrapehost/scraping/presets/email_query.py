ptags = document.find_all('p')


for ptag in ptags:
    if ptag.text:
        words = ptag.text.split(' ')

        for word in words:
            if '@' in word:
                if word not in self.data:
                    self.data.append(word)
