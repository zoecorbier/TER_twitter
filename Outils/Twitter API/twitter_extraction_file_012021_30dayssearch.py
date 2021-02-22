import tweepy
import json

consumer_key=''
consumer_secret=''
access_token=''
access_token_secret=''

#Authenticate
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

search_words = "suicide" 
#new_search = search_words + " -filter:retweets" #Ne fonctionne pas avec l'actuel package dev/search_full_archive

search_words ='suicide'
date_since = "201501010000"
date_to = "201501100000"
numTweets = 5

# premium search
tweets=tweepy.Cursor(api.search_full_archive,environment_name='devSOS', query=search_words, fromDate=date_since, toDate=date_to).items(numTweets)

for tweet in tweets:
    print(tweet.user.screen_name)
    print(tweet.text)
    print(tweet.user.location)
    