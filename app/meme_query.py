from meme_sources import MemeGenerator, KnowYourMeme
import search
import requests
import bs4

def get_memes_from_intents(intents):
    result = {}
    know_your_meme = KnowYourMeme()
    for key, url_list in intents.iteritems():
        result[key] = []
        for url in url_list:
            meme = know_your_meme.get_meme_from_url(url)
            result[key].append(meme.get_namespace())
    return result


def meme_query(query):
    meme_generator = MemeGenerator()
    return [meme for meme in meme_generator.get_memes(query)]


def main():
    # print(meme_query("cold"))
    base_url = 'http://knowyourmeme.com'
    popular_url = base_url + "/memes/popular"
    urls = set([])

    def fetch_page(url):
        try:
            search.get(url)
        except:
            res = requests.get(url)
            bs = bs4.BeautifulSoup(res.content)
            entries = bs.find('div', attrs={'id': 'entries_list'}).findAll('a')
            for url in entries:
                if url and url['href'].startswith('/memes/'):
                    urls.add(base_url + url['href'])

    fetch_page(popular_url)

    # get pages
    for page in range(100, 346):
        fetch_page(base_url + "/memes/popular/page/%d" % page)

    know_your_meme = KnowYourMeme()
    for url in urls:
        meme = know_your_meme.get_meme_from_url(url)
        search.submit(url, meme.get_namespace())
         #test_intents = {
    #    'critiques': [
    #        'http://knowyourmeme.com/memes/neil-degrasse-tyson-reaction'],
    #    'greetings': [
    #        'http://knowyourmeme.com/memes/night-of-nights-night-of-knights',
    #        'http://knowyourmeme.com/memes/luigi-wins-by-doing-absolutely-nothing']
    #    }
    #print(get_memes_from_intents(test_intents))

if __name__ == '__main__':
    main()
