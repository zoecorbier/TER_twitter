import os
import json
import datetime

import tweepy
# import csv
# import ssl
import time
from requests.exceptions import Timeout, ConnectionError
from requests.packages.urllib3.exceptions import ReadTimeoutError
import pandas as pd
import numpy as np
import logging
import mongo_db as db

import secrets

db_client = db.connection().tweet

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

def work(date_since = None , date_until = None, search_words = None):
    # Define the search term to make the search
    #search_words = "kill myself"
    logging.info(date_until)

    places=api.geo_search(query="USA", granularity="country")

    # Exclude retweets in our search
    new_search = search_words + " -place:"+places[0].id
    # + places[0].id
    '''Search for tweets created before a given date.
    Keep in mind that the Twitter Standard Search API has a 7-day limit.
    In other words, no tweets will be found for a date older than one week.'''
    #date_since = "2020-02-01"

    # Define until what date we are looking for tweets
    #date_until = "2020-02-02"

    # Total tweets to gather in our search
    totalTweets = 100

    # Numbers of tweets to return per page, max is 100. Default is 15.
    count = 100

    # Set the name for CSV file  where the tweets will be saved
    filename = "{}_{}".format(search_words,date_until)



    # # Function for handling pagination in our search
    # def limit_handled(cursor):
    #     while True:
    #         try:
    #             yield cursor.next()
    #         except tweepy.RateLimitError:
    #             print('Reached rate limite. Sleeping for >15 minutes')
    #             time.sleep(15 * 61)
            
    tweets = []
    for tweet in tweepy.Cursor(api.search_full_archive,
                                environment_name='devSOS',
                                query=new_search,
                                 fromDate=date_since,
                                 toDate=date_until,
                                 ).items(totalTweets):

        db.json_tweet_model(db_client,tweet._json,search_words)
        tweets.append(tweet)


    logging.info ("{}: {} tweets gathered".format(search_words, len(tweets)))
    print("{}: {} tweets gathered".format(search_words, len(tweets)))

    # current_file_path = os.path.dirname(os.path.realpath(__file__))
    # data_dir_path = os.path.normpath(os.path.join(current_file_path,'data'))
    # file_path = os.path.join(data_dir_path, filename)


    # with open(file_path+".json", 'w', encoding='utf-8') as f:
    #     json.dump(tweets, f, ensure_ascii=False)

    
if __name__ == "__main__":

    date_since = "201909010000"
    date_until = "202009200000"
    list_search_words = ["feel alone depressed","i feel helpless", "i feel sad","i feel empty","sleeping a lot lately","i feel irritable",
    "depressed alcohol","sertraline","Zoloft","Prozac","pills depressed","suicide once more", "pain suicide","mom suicide tried","friend suicide","sister suicide tried","Brother suicide tried",
    "suicide attempted sister", "thought suicide before", "had thoughts suicide","had thoughts killing myself", "i want to commit suicide", "stop cutting myself",
    "i'm being bullied", "feel bullied i'm", "stop bullying me","always getting bullied", "gun suicide", "been diagnosed anorexia", "i diagnosed OCD", "I diagnosed bipolar",
    "dad fight again", "parents fight again", "i impulsive", "i'm impulsive"]
    
    for search_word in list_search_words:
        work(date_since = date_since , date_until = date_until, search_words=search_word)