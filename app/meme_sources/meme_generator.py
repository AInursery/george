from meme_sources import MemeSource, MemeItem

from memoized_property import memoized_property
import bs4 as BeautifulSoup
import requests


class MemeGeneratorItem(MemeItem):

    def __init__(self, meme_soup):
        self.meme_soup = meme_soup

    # Soup accessors
    @memoized_property
    def title_soup(self):
        return self.meme_soup.find('a', attrs={'class': 'name'})

    @memoized_property
    def img_soup(self):
        return self.meme_soup.find('img')

    @memoized_property
    def url_soup(self):
        return self.meme_soup.find('a')

    @memoized_property
    def details_soup(self):
        request = requests.get(self.url)
        if request.status_code is 200:
            return BeautifulSoup.BeautifulSoup(request.content)

    @memoized_property
    def details_table_soup(self):
        return self.details_soup.find('table', {'class': 'table'})

    # Properties
    @memoized_property
    def title(self):
        title_soup = self.title_soup
        if title_soup:
            return title_soup['title']

    @memoized_property
    def url(self):
        url_soup = self.url_soup
        if url_soup:
            return '{0}{1}'.format(MemeGenerator.BASE_URL, url_soup['href'])

    @memoized_property
    def main_img(self):
        img_soup = self.img_soup
        if img_soup:
            return img_soup['src']

    @memoized_property
    def img_count(self):
        images_nb_row_soup = self.details_table_soup.findAll('tr')[0]
        return images_nb_row_soup.findAll('td')[1].text

    @memoized_property
    def score(self):
        images_nb_row_soup = self.details_table_soup.findAll('tr')[2]
        return images_nb_row_soup.findAll('td')[1].text[1:]


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
            memes_soup = gallery.findAll('li')
            for meme_soup in memes_soup:
                meme_item = MemeGeneratorItem(meme_soup)
                yield self._get_meme_namespace(meme_item)

    def _get_request(self, query):
        params = {'q': query}
        return requests.get('{0}{1}'.format(self.BASE_URL, self.API_URL),
                            params=params)

    def _get_meme_namespace(self, meme):
        result = {key: '' for key in ['title', 'img', 'url', 'img_count',
                                      'score']}
        title = meme.title
        img = meme.main_img
        url = meme.url
        img_count = meme.img_count
        score = meme.score

        if title:
            result['title'] = title
        if img:
            result['img'] = img
        if url:
            result['url'] = url
        if img_count:
            result['img_count'] = img_count
        if score:
            result['score'] = score
        return result
