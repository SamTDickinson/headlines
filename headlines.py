""" required import modules for application"""
import urllib
import urllib2
import json
import feedparser

from flask import Flask
from flask import render_template
from flask import request

APP = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS = {
    'publication' : 'bbc',
    'city' : 'London, UK'
}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?"+_
"q={}&units=metric&APPID=79f31e50e17bdba0f6162b4e16a3ae27"

@APP.route("/")
def home():
    """ Home function """
    # get customised headlines, based on user input or defaults.
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']

    articles = get_news(publication)

    # get customised weather based on user input of default
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)

    return render_template("home.html",
                           publication=publication.upper(),
                           articles=articles,
                           weather=weather)

def get_news(query):
    """ Returns the RSS feed for requested or Default publication """
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']

def get_weather(query):
    """ Returns weather for requested or default City"""
    query = urllib.quote(query)
    url = WEATHER_URL.format(query)
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
    