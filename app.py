#!/usr/bin/env python
#
# A party program with numbers
#

from flask import Flask, render_template, url_for, request

import re
import time
from pattern.web import Twitter

twitter = Twitter()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/get_twitter_data/<search_word>')
def get_twitter_data(search_word):
    #search_word = request.args.get('searchword', "SMI", type=int)
    for i in range(1, 3):
        for tweet in twitter.search('#' + search_word, start=i, count=2):
            # Parsing human date into INT
            date_time = re.sub('(\+\d{4})', '', tweet.date)
            timestamp = int(time.mktime(time.strptime(date_time, '%a %b %d %H:%M:%S %Y')))

            # Search for Hashtags
            s = tweet.text.lower()
            # print s
            hashtags = re.findall('(#\w+)', s)

    return render_template('index.html', hashtags=hashtags)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
