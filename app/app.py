"""
Penn Part of Speech Tags

Note:  these are the 'modified' tags used for Penn tree banking; these are the tags used in the Jet system. NP, NPS, PP, and PP$ from the original Penn part-of-speech tagging were changed to NNP, NNPS, PRP, and PRP$ to avoid clashes with standard syntactic categories.
1.	CC	Coordinating conjunction
2.	CD	Cardinal number
3.	DT	Determiner
4.	EX	Existential there
5.	FW	Foreign word
6.	IN	Preposition or subordinating conjunction
7.	JJ	Adjective
8.	JJR	Adjective, comparative
9.	JJS	Adjective, superlative
10.	LS	List item marker
11.	MD	Modal
12.	NN	Noun, singular or mass
13.	NNS	Noun, plural
14.	NNP	Proper noun, singular
15.	NNPS	Proper noun, plural
16.	PDT	Predeterminer
17.	POS	Possessive ending
18.	PRP	Personal pronoun
19.	PRP$	Possessive pronoun
20.	RB	Adverb
21.	RBR	Adverb, comparative
22.	RBS	Adverb, superlative
23.	RP	Particle
24.	SYM	Symbol
25.	TO	to
26.	UH	Interjection
27.	VB	Verb, base form
28.	VBD	Verb, past tense
29.	VBG	Verb, gerund or present participle
30.	VBN	Verb, past participle
31.	VBP	Verb, non-3rd person singular present
32.	VBZ	Verb, 3rd person singular present
33.	WDT	Wh-determiner
34.	WP	Wh-pronoun
35.	WP$	Possessive wh-pronoun
36.	WRB	Wh-adverb

"""
import os
from flask import Flask, jsonify
from textblob import TextBlob
from meme_query import meme_query


app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route("/api/<q>", methods=['GET', 'OPTIONS'])
def api(q):
    search_query = ""
    query = TextBlob(q)
    for sentense in query.sentences:
        # do some spell correction before adding it to the list
        sentense = sentense.correct()
        if sentense.noun_phrases:
            # Count the number the of time the noun apears in the whole query
            max_occurances = 0
            selected_noun = sentense.noun_phrases[0]
            for noun in sentense.noun_phrases:
                count_noun = query.count(noun)
                if max_occurances < count_noun:
                    max_occurances = count_noun
                    selected_noun = noun
            search_query = selected_noun
        else:  # it can be an interjection: hello!
            search_query = sentense
    res = meme_query(str(search_query))

    return jsonify({
        'author': 'George',
        'body': "<img src='%s' />" % res,
        'sentiment': query.sentiment.polarity
    })

if __name__ == "__main__":
    app.run(debug=True)
