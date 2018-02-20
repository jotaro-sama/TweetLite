# TweetLite
A little app to translate your Twitter description in japanese. 

# Configuration
To make it work on your server, be sure to install [python-oauth2](https://github.com/joestump/python-oauth2) in your virtual environment or machine.
You'll need to [register a Twitter app](https://apps.twitter.com/) and copy your oauth consumer key and consumer secret from the app page. Then, you'll need to create a file named `.twapicred` inside the `mainsite` folder, and format it like this:
```
oauth_consumer_key: {your oauth consumer key}
oauth_callback: {url where your main website resides}/logged/
consumer_secret: {your oauth consumer secret}
```
The server currently supports the default port (8000) only. Multiple port support to be added in the future.
You'll also need to set appropriate IBM Watson credentials. Details in the Translator API section.

To run the server with default values, just run the following:
```
python3 manage.py makemigrations translator
python3 manage.py makemigrations mainsite
python3 manage.py migrate
python3 manage.py runserver
```

# Translator API
The translator is a REST service powered by IBM Watson. It translates a given text to Japanese. In order to make it work, you must have [the Python SDK for Watson Developer Cloud](https://pypi.python.org/pypi/watson-developer-cloud) installed in your server's. Furthermore, your server must connect to [an instance of IBM Watson's Translator service](https://www.ibm.com/watson/developer-resources/). After registering an account and creating a Translator instance, put your encrypted username and password in a file named `.ibmwcred` inside the `translator` folder. `.ibmwcred` must be in the format: 
```
username: {username}
password: {password}
```
To use it, the client must submit a GET request with a `text` parameter containing the text to translate (e.g. `127.0.0.1:8000/translator/?text={text to translate}`). For some reason it works better with sentences, single words may give weird results, expecially if from languages other than english.