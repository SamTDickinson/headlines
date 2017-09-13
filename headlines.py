
import feedparser
from flask import Flask 
from flask import render_template
APP = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

@APP.route("/")
@APP.route("/<publication>")

def get_news(publication="bbc"):
    """ Returns the first RSS feed """
    feed = feedparser.parse(RSS_FEEDS[publication])
    return render_template("home.html", publication=publication, articles=feed['entries'])

if __name__ == '__main__':
    APP.run(port=5000, debug=True)
    