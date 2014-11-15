import requests
import bs4 as BeautifulSoup

BASE_URL = 'http://memegenerator.net'
API_URL = '/memes/search'


def meme_query(query):
    return [meme for meme in meme_query_all(query)]


def meme_query_all(query):
    params = {'q': query}
    res = requests.get('{0}{1}'.format(BASE_URL, API_URL), params=params)
    if res.status_code is 200:
        # Got an answer
        soup = BeautifulSoup.BeautifulSoup(res.content)
        meme_horizontal_gallery = soup.find('ul',
            attrs={'class': u'horizontal'})
        memes = meme_horizontal_gallery.findAll('li')
        for meme in memes:
            result = {
                'img': '',
                'title': '',
                'url': ''
            }
            meme_url = meme.find('a')
            if meme_url:
                result['url'] = '{0}{1}'.format(BASE_URL, meme_url['href'])
            meme_img = meme_url.find('img')
            if meme_img:
                result['img'] = meme_img['src']
            meme_title = meme.find('a',
                attrs={'class': 'name'})
            if meme_title:
                result['title'] = meme_title['title']
            yield result


def main():
    print(meme_query("cold"))

if __name__ == '__main__':
    main()
