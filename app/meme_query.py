import requests
import bs4 as BeautifulSoup

API_URL = 'http://memegenerator.net/memes/search'


def meme_query(query):
    params = {'q': query}
    res = requests.get(API_URL, params=params)
    if res.status_code is 200:
        # Got an answer
        soup = BeautifulSoup.BeautifulSoup(res.content)
        meme_horizontal_gallery = soup.find('ul',
            attrs={'class': u'horizontal'})
        first_meme = meme_horizontal_gallery.find('li')
        first_meme_img = first_meme.find('img')
        return first_meme_img['src']
    else:
        # Error : TODO
        return None


def main():
    meme_query("cold")

if __name__ == '__main__':
    main()
