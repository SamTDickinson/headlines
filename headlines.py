import feedparser
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
    return render_template("home.html", publication=publication.upper(), articles=feed['entries'])

if __name__ == '__main__':
    APP.run(port=5000, debug=True)
    