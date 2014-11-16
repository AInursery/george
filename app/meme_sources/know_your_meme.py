from meme_sources import MemeSource, MemeItem

from memoized_property import memoized_property
import bs4 as BeautifulSoup
import requests


class KnowYourMemeItem(MemeItem):

    def __init__(self, meme_soup):
        self.meme_soup = meme_soup

    # Soup accessors
    @memoized_property
    def header_soup(self):
        return self.meme_soup.find('div', {'id': 'content'}).find('header')

    @memoized_property
    def info_soup(self):
        return self.header_soup.find('section', {'class': 'info'})

    @memoized_property
    def stats_soup(self):
        return self.info_soup.find('aside', {'class': 'stats'})

    @memoized_property
    def entry_body_soup(self):
        return self.meme_soup.find('div', {'id': 'entry_body'})

    # Properties
    @memoized_property
    def title(self):
        info_soup = self.info_soup
        h1_soup = info_soup.find('h1')
        if h1_soup:
            return h1_soup.find('a').text

    @memoized_property
    def url(self):
        info_soup = self.info_soup
        relative_url = info_soup.find('h1').find('a')['href']
        return '{0}{1}'.format(KnowYourMeme.BASE_URL, relative_url)

    @memoized_property
    def main_img(self):
        return self.header_soup.find('a', {'class': 'photo'})['href']

    @memoized_property
    def img_count(self):
        stats_soup = self.stats_soup
        return stats_soup.find('dd', {'class': 'photos'}).find('a').text

    @memoized_property
    def score(self):
        stats_soup = self.stats_soup
        return stats_soup.find('dd', {'class': 'views'}).find('a').text

    @memoized_property
    def tags(self):
        entry_soup = self.entry_body_soup
        tag_soups = entry_soup.find('dl', {'id': 'entry_tags'}).findAll('a')
        return [tag_soup.text for tag_soup in tag_soups]

    def get_namespace(self):
        properties = ['title', 'main_img', 'url', 'img_count',
                      'score', 'tags']
        result = {key: '' for key in properties}

        for key in properties:
            value = getattr(self, key)
            if value:
                result[key] = value
        return result


class KnowYourMeme(MemeSource):
    """docstring for KnowYourMeme"""

    BASE_URL = 'http://knowyourmeme.com'

    def get_memes(self, query):
        pass

    def get_meme_from_url(self, url):
        request = requests.get(url)
        if request.status_code is 200:
            # Get the html soup
            request_soup = BeautifulSoup.BeautifulSoup(request.content)
            return KnowYourMemeItem(request_soup)

    def _get_meme_namespace(self, meme):
        pass
