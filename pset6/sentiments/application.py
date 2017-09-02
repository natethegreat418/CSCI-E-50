"""Fetches tweets from Twitter based on user input, analyzes the sentiment of each tweet and charts them"""
from flask import Flask, redirect, render_template, request, url_for

import helpers
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name, if invalid go to homepage
    screen_name = request.args.get("screen_name", "").lstrip("@")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets, if none go to homepage
    tweets = helpers.get_user_timeline(screen_name)
    if len(tweets) < 1:
        return redirect(url_for("index"))
    
    # absolute paths to lists
    positives = "positive-words.txt"
    negatives = "negative-words.txt"

    # instantiate analyzer
    analyzer = Analyzer(positives, negatives)

    p, n, ne = 0, 0, 0
    
    # for each tweet retrieved, employ analyzer
    for t in tweets:
        score = analyzer.analyze(t)
        # score tweet and count score
        if score > 0.0:
            p += 1
        elif score < 0.0:
            n += 1
        else:
            ne += 1
            
    positive, negative, neutral = p, n, ne

    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
