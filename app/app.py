import os
import requests
import random
from urllib import quote
from flask import Flask, jsonify
import search
from meme_query import meme_query
from meme_sources import KnowYourMeme


app = Flask(__name__)

WIT_URL = "https://api.wit.ai/message?v=20141116&q="
ses = requests.Session()
ses.headers.update({'Authorization': 'Bearer 5VKYLUWKTBBUYRR22WAO7IATAGFQR5U4'})

intent_memes = {
    'greetings': [
        'http://knowyourmeme.com/memes/yes-this-is-dog',
        'http://knowyourmeme.com/memes/im-an-anteater',
        'http://knowyourmeme.com/memes/hello-my-future-girlfriend',
    ],
    'affirmations': [
        'http://knowyourmeme.com/memes/you-dont-say',
        'http://knowyourmeme.com/memes/true-story',
        'http://knowyourmeme.com/memes/futurama-fry-not-sure-if',
        'http://knowyourmeme.com/memes/u-wot-m8',
    ],
    'critiques': [
        'http://knowyourmeme.com/memes/neil-degrasse-tyson-reaction',
        'http://knowyourmeme.com/memes/haters-gonna-hate',
        'http://knowyourmeme.com/memes/disaster-girl',
        'http://knowyourmeme.com/memes/look-at-all-the-fucks-i-give',
        'http://knowyourmeme.com/memes/come-at-me-bro',
        'http://knowyourmeme.com/memes/prepare-your-anus',
        'http://knowyourmeme.com/memes/im-sorry-i-cant-hear-you-over-the-sound-of-how-awesome-i-am',
        'http://knowyourmeme.com/memes/thats-racist',
        'http://knowyourmeme.com/memes/wtf-is-this-shit'
    ],
    'personal_questions': [
        'http://knowyourmeme.com/memes/obama-rage-face-not-bad',
        'http://knowyourmeme.com/memes/upvoting-obama',
        #'http://knowyourmeme.com/memes/chuck-norris-facts',
    ],
    'compliments': [
        'http://knowyourmeme.com/memes/good-guy-greg',
        'http://knowyourmeme.com/memes/fck-yea',
        'http://knowyourmeme.com/memes/60s-spider-man',
        'http://knowyourmeme.com/memes/10-guy',
        'http://knowyourmeme.com/memes/joseph-ducreux-archaic-rap',
        'http://knowyourmeme.com/memes/freddie-mercury-rage-pose',
        'http://knowyourmeme.com/memes/success-kid-i-hate-sandcastles',
        'http://knowyourmeme.com/memes/brent-rambo'
    ],
    'questions': [
        'http://knowyourmeme.com/memes/i-like-turtles',
        'http://knowyourmeme.com/memes/ancient-aliens',
        'http://knowyourmeme.com/memes/no-rage-face',
        'http://knowyourmeme.com/memes/grumpy-cat',
        'http://knowyourmeme.com/memes/o-rly',
        'http://knowyourmeme.com/memes/i-dunno-lol-_o'
    ]
}

@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route("/api/<q>", methods=['GET', 'OPTIONS'])
def api(q):

    es_meme = None
    wit_res = ses.get(WIT_URL + quote(q))
    if wit_res.status_code == 200:
        wit_json = wit_res.json()
        for outcome in wit_json['outcomes']:
            if outcome['confidence'] < 0.4:
                break

            intent = outcome['intent']
            if intent in intent_memes:
                url = random.choice(intent_memes[intent])
                try:
                    es_meme = search.get(url)
                except:
                    know_your_meme = KnowYourMeme()
                    source = know_your_meme.get_meme_from_url(url)
                    data = source.get_namespace()
                    search.submit(url, data)
                    es_meme = search.get(url)

    # do a fuzzy search
    if not es_meme:
        es_meme = search.search(q)[0]

    return jsonify({
        'author': 'George',
        'body': """
        <p>
            <a href='{url}' title="{title}"><img src='{main_img}' alt="{title}" /></a>
        </p>
        """.format(**es_meme['_source']),
    })


port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
    app.run(port=int(port), debug=True)
