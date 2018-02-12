# TweetLite
A very lightweigtht app to read the latest tweets from your profile. It also translates your bio in japanese.

# Translator API
The translator is powered by IBM Watson. It translates a given text to Japanese. In order to make it work, you must have [the Python SDK for Watson Developer Cloud](https://pypi.python.org/pypi/watson-developer-cloud) installed in your server's. Furthermore, your server must connect to [an instance of IBM Watson's Translator service](https://www.ibm.com/watson/developer-resources/). After registering an account and creating a Translator instance, put your encrypted username and password in a file named `.ibmwcred` inside the `translator` folder. `.ibmwcred` must be in the format: 
```
username: {username}
password: {password}
```
To use it, the client must submit a GET request with a `text` parameter containing the text to translate (e.g. `127.0.0.1:8000/translator/?text={text to translate}`). For some reason it works better with sentences, single words may give weird results, expecially if from languages other than english.
