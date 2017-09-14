""" required import modules for application"""
import urllib
import urllib2
import json
import datetime
import feedparser

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response

APP = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS = {
    'publication' : 'bbc',
    'city' : 'London, UK',
    'currency_from' : 'GBP',
    'currency_to' : 'USD'
}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=79f31e50e17bdba0f6162b4e16a3ae27"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=a010a8aa4c284792bdfbfb4b0e9b2367"


def get_value_with_fallback(key):
    """ get request, cookie or default user values """
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]

@APP.route("/")

def home():
    """ Home function """
    # get customised headlines, based on user input or defaults.
    publication = get_value_with_fallback('publication')
    articles = get_news(publication)

    # get customised weather based on user input of default
    city = get_value_with_fallback('city')
    weather = get_weather(city)

    currency_from = get_value_with_fallback('currency_from')
    currency_to = get_value_with_fallback('currency_to')
    rate, currencies = get_currency(currency_from, currency_to)

    response = make_response(
        render_template("home.html",
                        publication=publication.upper(),
                        articles=articles,
                        weather=weather,
                        currency_from=currency_from,
                        currency_to=currency_to,
                        rate=rate,
                        currencies=sorted(currencies)))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)

    return response



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
                   "temperature" : parsed["main"]["temp"],
                   "city" : parsed["name"],
                   "country" : parsed['sys']['country']
                  }
    return weather

def get_currency(c_frm, c_to):
    """ returns currency rates for requested of default value """
    all_currency = urllib2.urlopen(CURRENCY_URL)

    parsed = json.load(all_currency).get('rates')
    frm_rate = parsed.get(c_frm.upper())
    to_rate = parsed.get(c_to.upper())
    return (to_rate/frm_rate, parsed.keys())

if __name__ == '__main__':
    APP.run(port=5000, debug=True)
    