# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 16:49:37 2020

@author: Lucas
"""
import tweepy
import csv
import ssl
import time
from requests.exceptions import Timeout, ConnectionError
from requests.packages.urllib3.exceptions import ReadTimeoutError
import json

''' More info on Standard Search API:
https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html'''

# Add your Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

# Handling authentication with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

# Create a wrapper for the API provided by Twitter
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
places=api.geo_search(query="Canada", granularity="country")
print(places[0])

# Define the search term to make the search
search_words = "Suicide"

# Exclude retweets in our search
new_search = search_words + " -filter:retweets place:" + places[0].id

'''Search for tweets created before a given date.
Keep in mind that the Twitter Standard Search API has a 7-day limit.
In other words, no tweets will be found for a date older than one week.'''
date_since = "2020-03-01"

# Define until what date we are looking for tweets
date_until = ""

# Total tweets to gather in our search
totalTweets = 10000

# Numbers of tweets to return per page, max is 100. Default is 15.
count = 100

# Filter by language
lang = "fr"

'''Filter by latitude,longitude,radius.
# 37.781157 -122.398720 1mi'''
geocode = ""

# Filter by recent, popular or mixed.
result_type = "recent"

'''Include info on entities found in Tweets, including hashtags,
links, and mentions. Set to True or False'''
include_entities = True

# Set the name for CSV file  where the tweets will be saved
filename = "depression"

test=[]
# Function for handling pagination in our search
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print('Reached rate limite. Sleeping for >15 minutes')
            time.sleep(15 * 61)


# Function for make the search using Twitter API
def search_tweets(new_search, date_since):

    # performs the search using the defined variables
    for tweet in limit_handled(tweepy.Cursor(api.search,
                               q=new_search,
                               count=count,
                               tweet_mode='extended',
                               lang=lang,
                               #geocode=geocode,
                               result_type=result_type,
                               include_entities=include_entities,
                               since=date_since,
                               until=date_until).items(totalTweets)):

        try:

            # Checks if its a extended tweet (>140 characters)
            content = tweet.full_text
            print(content)

            '''Convert all named and numeric character references
            (e.g. &gt;, &#62;, &#x3e;) in the string s to the
            corresponding Unicode characters'''
            content = (content.replace('&amp;', '&').replace('&lt;', '<')
                       .replace('&gt;', '>').replace('&quot;', '"')
                       .replace('&#39;', "'").replace(';', " ")
                       .replace(r'\u', " ").replace('\u2026', ""))

            # Save other information from the tweet
            user = tweet.author.screen_name
            timeTweet = tweet.created_at
            source = tweet.source
            tweetId = tweet.id
            tweetUrl = "https://twitter.com/statuses/" + str(tweetId)
            tweetPlace=tweet.author.location
            test.append(tweet)
            # Exclude retweets, too many mentions and too many hashtags
            if not any((('RT @' in content, 'RT' in content,
                       content.count('@') >= 2, content.count('#') >= 3))):

                # Saves the tweet information in a new row of the CSV file
                writer.writerow([content, timeTweet,
                                user,source, tweetId,tweetUrl,tweetPlace])

        except Exception as e:
            print('Encountered Exception:', e)
            pass



def work():

    # Opening a CSV file to save the gathered tweets
    with open(filename+".csv", 'w') as file:
        global writer
        writer = csv.writer(file)

        # Initializing the Twitter search
        try:
            search_tweets(search_words, date_since)

        # Stop temporarily when hitting Twitter rate Limit
        except tweepy.RateLimitError:
            print("RateLimitError...waiting ~15 minutes to continue")
            time.sleep(1001)
            search_tweets(search_words, date_since)

        # Stop temporarily when getting a timeout or connection error
        except (Timeout, ssl.SSLError, ReadTimeoutError,
                ConnectionError) as exc:
            print("Timeout/connection error...waiting ~15 minutes to continue")
            time.sleep(1001)
            search_tweets(search_words, date_since)

        # Stop temporarily when getting other errors
        except tweepy.TweepError as e:
            if 'Failed to send request:' in e.reason:
                print("Time out error caught.")
                time.sleep(1001)
                search_tweets(search_words, date_since)
            elif'Too Many Requests' in e.reason:
                print("Too many requests, sleeping for 15 min")
                time.sleep(1001)
                search_tweets(search_words, date_since)
            else:
                print(e)
                print("Other error with this user...passing")
                pass


if __name__ == '__main__':

    work()
