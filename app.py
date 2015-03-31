#!/usr/bin/env python
#
# A party program with numbers
#

from flask import Flask, render_template, request, url_for
import base64, json, re, time
from pattern.web    import Twitter
from pattern.graph  import Graph

# Define pattern
key          = "2nee4DogHlJLxu6zMD0E0JxH6"
secret       = "YdEYUvgDPLeUhWgQpNxd3cK1StcHiA6HQd4kxWIbj4C5BsH3ZW"
token        = "81363798-2ZHf3BvCH0V4k5nIOZbGQfkur3xonkZCKsQeAenLf"
token_secret = "m9AQyL3V7gclxyWprYEuqUGje26jTCuTfwMrKrTW6NmKb"
twitter_license = (key, secret, (token, token_secret))
# (
#     "p7HUdPLlkKaqlPn6TzKkA", # OAuth (key, secret, token)
#     "R7I1LRuLY27EKjzulutov74lKB0FjqcI2DYRUmsu7DQ", (
#     "14898655-TE9dXQLrzrNd0Zwf4zhK7koR5Ahqt40Ftt35Y2qY",
#     "q1lSRDOguxQrfgeWWSJgnMHsO67bqTd5dTElBsyTM"))

# twitter = Twitter(license=base64.b64encode(s), throttle=0.5, language='en')
twitter = Twitter(license=twitter_license, throttle=0.5, language='en')
# twitter = Twitter()
# twitter.license              # Service license key.
# twitter.throttle             # Time between requests (being nice to server).
# twitter.language             # Restriction for Result.language (e.g., 'en').

def get_hashtags(search_word, g, ignore_words, recursion_depth):
    # Get the first 2 results ...
    for i in range(1, 3):
        for tweet in twitter.search('#' + search_word, start=i, count=2):
            # Parsing human date into INT
            date_time = re.sub('(\+\d{4})', '', tweet.date)
            timestamp = int(time.mktime(time.strptime(date_time, '%a %b %d %H:%M:%S %Y')))

            # Search for Hashtags
            s = tweet.text.lower()
            # print s
            hashtags = re.findall('(#\w+)', s)
            ignore_words.append(search_word)

            # Store as network
            for tag in hashtags:
                g.add_node(tag)
                g.add_edge(search_word, tag, weight=0.0, type='is-related-to')
                if tag not in ignore_words or recursion_depth > -1:
                    g, ignore_words, recursion_depth = get_hashtags(tag, g, ignore_words, recursion_depth-1)

            return g, ignore_words, recursion_depth+1

# Define routes
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# @app.route('/get_twitter_data/<search_word>')
# def get_twitter_data(search_word):
@app.route('/get_twitter_data')
def get_twitter_data():

    # Get seach-term
    search_word = request.args.get('search_term')
    search_word = search_word[1:] if search_word[0] == '#' else search_word
    print search_word

    # Define Graph
    g = Graph()
    g.add_node(search_word)

    ignore_words = []; recursion_depth = 2
    # Get the first 2 results ...
    for i in range(1, 3):
        for tweet in twitter.search('#' + search_word, start=i, count=2):
            # Parsing human date into INT
            date_time = re.sub('(\+\d{4})', '', tweet.date)
            timestamp = int(time.mktime(time.strptime(date_time, '%a %b %d %H:%M:%S %Y')))

            # Search for Hashtags
            s = tweet.text.lower()
            # print s
            hashtags = re.findall('(#\w+)', s)
            ignore_words.append(search_word)

            # Store as network
            for tag in hashtags:
                g.add_node(tag)
                g.add_edge(search_word, tag, weight=0.0, type='is-related-to')
                if tag not in ignore_words or recursion_depth > -1:
                    g, ignore_words, recursion_depth = get_hashtags(tag, g, ignore_words, recursion_depth-1)

    return g.serialize('data') # html | css | canvas | data


@app.route('/get_twitter_trends')
def get_twitter_trends():
    trends = twitter.trends(cached=False)
    return render_template('subgroup.html', trends=trends)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
