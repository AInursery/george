from elasticsearch import Elasticsearch
from pprint import pprint as pp

es = Elasticsearch()

INDEX = "meme-index"
TYPE = "meme"


def submit(id, doc):
    res = es.index(index=INDEX, doc_type=TYPE, id=id, body=doc)
    if res['created']:
        return True


def search(query):
    es.indices.refresh(index=INDEX)
    res = es.search(index=INDEX, body={
        "query": {
            "fuzzy_like_this": {
                "fields": ["title"],
                "like_text": query,
                "max_query_terms": 12
            }
        }
    })

    print("Query: %s -> Got %d Hits:" % (query, res['hits']['total']))
    return res['hits']['hits']

def get(id):
    """
    :param id: the exact match of the id (the url)
    :return: dict
    """""
    return es.get(index=INDEX, doc_type=TYPE, id=id)


if __name__ == '__main__':
    #es.indices.delete(index=INDEX)
    #submit("http://www.google.com/", {
     #   'title': "hello world",
     #   'body': "body ",
     #   'img': 'url'
    #})
    #res = search("how")
    res = get('http://knowyourmeme.com/memes/pancake-bunny')
    pp(res)
    #res = search("hi")
