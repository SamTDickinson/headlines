import feedparser
import json
import urllib2
import urllib

from flask import Flask
from flask import render_template
from flask import request

APP = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

@APP.route("/")
def get_news():
    """ Returns the first RSS feed """
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    weather = get_weather("London, UK")
    return render_template("home.html", 
                           publication=publication.upper(),
                           articles=feed['entries'],
                           weather=weather)

def get_weather(query):
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=79f31e50e17bdba0f6162b4e16a3ae27'
    query = urllib.quote(query)
    url = api_url.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description":
                   parsed["weather"][0]["description"],
                   "temperature":parsed["main"]["temp"],
                   "city":parsed["name"]
                  }
    return weather

if __name__ == '__main__':
    APP.run(port=5000, debug=True)
    