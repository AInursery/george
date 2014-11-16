from meme_sources import MemeSource

import bs4 as BeautifulSoup
import requests


class MemeGenerator(MemeSource):
    """docstring for MemeGenerator"""

    BASE_URL = 'http://memegenerator.net'
    API_URL = '/memes/search'

    def get_memes(self, query):
        request = self._get_request(query)
        if request.status_code is 200:
            # Get the html soup
            request_soup = BeautifulSoup.BeautifulSoup(request.content)
            # Extract the gallery of memes
            gallery = request_soup.find('ul', attrs={'class': u'horizontal'})
            # Each list element is a meme
            memes = gallery.findAll('li')
            for meme in memes:
                meme_url = meme.find('a')
                meme_img = meme_url.find('img')
                meme_title = meme.find('a', attrs={'class': 'name'})
                yield self._get_meme_namespace(meme_title, meme_img, meme_url)

    def _get_request(self, query):
        params = {'q': query}
        return requests.get('{0}{1}'.format(self.BASE_URL, self.API_URL),
                            params=params)

    def _get_meme_namespace(self, title_soup, img_soup, url_soup):
        result = {key: '' for key in ['title', 'img', 'url']}
        if title_soup:
            result['title'] = title_soup['title']
        if img_soup:
            result['img'] = img_soup['src']
        if url_soup:
            result['url'] = '{0}{1}'.format(self.BASE_URL, url_soup['href'])
        return result