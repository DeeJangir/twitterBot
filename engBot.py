from flask_api import FlaskAPI
from flask import request

app = FlaskAPI(__name__)

def getMessage(wordSupply = None):
    import json
    import random
    import tweepy
    from PyDictionary import PyDictionary
    from googletrans import Translator
    translator = Translator()

    auth = tweepy.OAuthHandler("CONSUMER_KEY", "CONSUMER_SECRET")
    auth.set_access_token("ACCESS_TOKEN", "ACCESS_TOKEN_SECRET")
    tweeterApi = tweepy.API(auth)
    dic = PyDictionary()

    if wordSupply:
        generatedWord = wordSupply
    else:
        with open("wordList.json") as fo:
            data = json.load(fo)
            generatedWord = random.choice(data)
    print(generatedWord, "------ generated word")
    meaningData = dic.meaning(generatedWord)

    try:
        tweetMsg = ""
        tweetMsg += "Word: " + generatedWord.capitalize() + "\n"
        for key in meaningData.keys():
            oneByOne = meaningData[key]
            if len(oneByOne) != 0:
                tweetMsg += key + ": " + oneByOne[0].capitalize() + "\n"
        tweetMsg += "French Word: "+ str(translator.translate(generatedWord, dest='fr').text).capitalize() +"\n"
        tweetMsg += "#"+generatedWord + " #engBotPy"

        print(tweetMsg)
        try:
            tweeterApi.update_status(tweetMsg)
            return tweetMsg
        except tweepy.error.TweepError:
            return {"error_msg":"tweet already present"}
    except AttributeError:
        return {"error_msg":"No definition found"}
    print(meaningData)

@app.route('/doTweet/')
def doTweet():
    
    return {'tweetMsg': getMessage()}

@app.route("/doTweet/<string:key>/")
def notes_detail(key):

    return getMessage(key)

if __name__ == "__main__":
    app.run(debug=False)
