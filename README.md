george
======

George the Meme Bot !

Ask George something and he'll respond with an Internet Meme.


Install
-------

You need to install an elasticsearch instance localy to use this bot. Also an wit.ai account is required.

```
git clone https://github.com/AInursery/george
cd george
virtualenv .
pip install -r requirements.txt
```

Populate the elasticsearch db with the data from knowyourmeme.com using this script: 

```
python app/meme_query.py #  it will take a very very long time to fetch all the data. Use and existing db or limit your queries for testing
``` 

Running
-------

```
python app/app.py
```

Go to: http://localhost:5000/#/

License
-------

Apache
