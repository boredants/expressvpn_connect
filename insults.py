
def insults():
    """Grab an insult and print it
    to the screen"""
    
    import requests
    from bs4 import BeautifulSoup

    url = 'http://randominsults.net' 

    r = requests.get(url)

    html = r.text

    soup = BeautifulSoup(html, 'lxml')

    for tag in soup.find_all('strong'):
        print(tag.text)
