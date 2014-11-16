from meme_sources import MemeGenerator, KnowYourMeme


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
    test_intents = {
        'critiques': [
            'http://knowyourmeme.com/memes/neil-degrasse-tyson-reaction'],
        'greetings': [
            'http://knowyourmeme.com/memes/night-of-nights-night-of-knights',
            'http://knowyourmeme.com/memes/luigi-wins-by-doing-absolutely-nothing']
        }
    print(get_memes_from_intents(test_intents))

if __name__ == '__main__':
    main()
