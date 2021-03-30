import os
import json
import datetime

import tweepy
# import csv
# import ssl
# import time
# from requests.exceptions import Timeout, ConnectionError
# from requests.packages.urllib3.exceptions import ReadTimeoutError
import pandas as pd
import numpy as np
import logging
import sys
import mongo_db as mongo


import secrets


logging.basicConfig(filename='import.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',  datefmt='%d-%b-%y', level=logging.INFO)


''' More info on Standard Search API:
https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html'''

# Add your Twitter API credentials
consumer_key = secrets.consumer_key
consumer_secret = secrets.consumer_secret
access_key = secrets.access_key
access_secret = secrets.access_secret

# Handling authentication with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

# Create a wrapper for the API provided by Twitter
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
def work(date_since, date_until, search_words):
    # Define the search term to make the search
    #search_words = "kill myself"
    logging.info(date_until)
    places=api.geo_search(query="USA", granularity="country")

    # Exclude retweets in our search
    new_search = search_words + " -filter:retweets place:" + places[0].id

    '''Search for tweets created before a given date.
    Keep in mind that the Twitter Standard Search API has a 7-day limit.
    In other words, no tweets will be found for a date older than one week.'''
    date_since = "202102211500"

    # Define until what date we are looking for tweets
    #date_until = "2020-02-02"

    # Total tweets to gather in our search
    totalTweets = 10000

    # Numbers of tweets to return per page, max is 100. Default is 15.
    count = 100

    # Filter by language
    lang = "en"

    '''Filter by latitude,longitude,radius.
    # 54.375675 -3.764280 1948mi'''
    geocode = "54,12 -4,00 315mi"

    # Filter by recent, popular or mixed.
    result_type = "recent"

    '''Include info on entities found in Tweets, including hashtags,
    links, and mentions. Set to True or False'''
    include_entities = True

    # Set the name for CSV file  where the tweets will be saved
    filename = "{}_{}".format(search_words,date_until)

    # # Function for handling pagination in our search
    # def limit_handled(cursor):
    #     keep_going = True
    #     while keep_going:
    #         try:
    #             try:
    #                 yield cursor.next()
    #             except StopIteration:
    #                 keep_going = False
    #         except (tweepy.RateLimitError) as e:
    #             print(e)
    #             print('Reached rate limite. Sleeping for >30 secondes')
    #             time.sleep(1 * 30)

    # Function for handling pagination in our search
    def limit_handled(cursor):
        while True:
            try:
                yield cursor.next()
            except tweepy.RateLimitError:
                print('Reached rate limite. Sleeping for >15 minutes')
                time.sleep(15 * 61)
    db = mongo.connection().tweet 
    # tweets = []
    for tweet in limit_handled(tweepy.Cursor(api.search_30_day,
                                environment_name='devSOS',
                                query=search_words
                                 ).items(totalTweets)):

        mongo.json_tweet_model(db,tweet._json,search_word)
    #     tweets.append(tweet._json)

    # logging.info ("{}: {} tweets gathered".format(search_words, len(tweets)))
    # print("{}: {} tweets gathered".format(search_words, len(tweets)))

    # current_file_path = os.path.dirname(os.path.realpath(__file__))
    # data_dir_path = os.path.normpath(os.path.join(current_file_path,'data'))
    # file_path = os.path.join(data_dir_path, filename)


    with open(file_path+".json", 'w', encoding='utf-8') as f:
        json.dump(tweets, f, ensure_ascii=False)

    
if __name__ == "__main__":

    date_since = ""
    date_until = str(datetime.date.today())
    list_search_words = ["feel alone depressed","i feel helpless", "i feel sad","i feel empty","sleeping a lot lately","i feel irritable",
    "depressed alcohol","sertraline","Zoloft","Prozac","pills depressed","suicide once more", "pain suicide","mom suicide tried","friend suicide","sister suicide tried","Brother suicide tried",
    "suicide attempted sister", "thought suicide before", "had thoughts suicide","had thoughts killing myself", "i want to commit suicide", "stop cutting myself",
    "i'm being bullied", "feel bullied i'm", "stop bullying me","always getting bullied", "gun suicide", "been diagnosed anorexia", "i diagnosed OCD", "I diagnosed bipolar",
    "dad fight again", "parents fight again", "i impulsive", "i'm impulsive"]
    
    for search_word in ["suicide"]:
        work(date_since, date_until, search_word)