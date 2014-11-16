from meme_sources import MemeGenerator


def meme_query(query):
    meme_generator = MemeGenerator()
    return [meme for meme in meme_generator.get_memes(query)]


def main():
    print(meme_query("cold"))


if __name__ == '__main__':
    main()
