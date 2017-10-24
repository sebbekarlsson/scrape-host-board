detail = document.find('div', {'class': 'user-details'})

if detail:
    a = detail.find('a')
    
    if a:
        username = a.text

        if username not in self.data:
            self.data.append(username)
