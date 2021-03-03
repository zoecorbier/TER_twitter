import mongo_db

db=mongo_db.connection('tweet')

##Test insertion

json={
    'created_at': 'Wed Apr 30 23:59:40 +0000 2014',
    'id': 461656162237034496,
    'id_str': '461656162237034496',
    'text': '#NEW #OFFICIAL "SUICIDE NOTE" #VIDEO FROM @IamPoppCulture via @youtube &gt;http://t.co/Ech4loAtWx&lt; #MuzikkZone x5',
    'source': '<a href="http://blackberry.com/twitter" rel="nofollow">Twitter for BlackBerry®</a>',
    'truncated': False,
    'in_reply_to_status_id': None,
    'in_reply_to_status_id_str': None,
    'in_reply_to_user_id': None,
    'in_reply_to_user_id_str': None,
    'in_reply_to_screen_name': None,
    'user': {
        'id': 1677894596,
        'id_str': '1677894596',
        'name': 'Princess Rina',
        'screen_name': 'Princess3Rina',
        'location': '#JetSetLife',
        'url': 'https://www.twitter.com/princess3rina',
        'description': 'Official Twitter Account For #PrincessRina #MuzikkZone A Malaysian Royalty 🚫PORN',
        'translator_type': 'regular',
        'protected': False,
        'verified': False,
        'followers_count': 121420,
        'friends_count': 46501,
        'listed_count': 304,
        'favourites_count': 423760,
        'statuses_count': 617334,
        'created_at': 'Sat Aug 17 10:25:59 +0000 2013',
        'utc_offset': None,
        'time_zone': None,
        'geo_enabled': True,
        'lang': None,
        'contributors_enabled': False,
        'is_translator': False,
        'profile_background_color': 'FF6699',
        'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme11/bg.gif',
        'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme11/bg.gif',
        'profile_background_tile': True,
        'profile_link_color': 'B40B43',
        'profile_sidebar_border_color': 'CC3366',
        'profile_sidebar_fill_color': 'E5507E',
        'profile_text_color': '362720',
        'profile_use_background_image': True,
        'profile_image_url': 'http://pbs.twimg.com/profile_images/1223136817387425797/o8pHI8MF_normal.jpg',
        'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1223136817387425797/o8pHI8MF_normal.jpg',
        'profile_banner_url': 'https://pbs.twimg.com/profile_banners/1677894596/1568075051',
        'default_profile': False,
        'default_profile_image': False,
        'following': None,
        'follow_request_sent': None,
        'notifications': None
    },
    'geo': None,
    'coordinates': None,
    'place': None,
    'contributors': None,
    'is_quote_status': False,
    'quote_count': 0,
    'reply_count': 0,
    'retweet_count': 0,
    'favorite_count': 0,
    'entities': {
        'hashtags': [{
            'text': 'NEW',
            'indices': [0, 4]
        }, {
            'text': 'OFFICIAL',
            'indices': [5, 14]
        }, {
            'text': 'VIDEO',
            'indices': [30, 36]
        }, {
            'text': 'MuzikkZone',
            'indices': [102, 113]
        }],
        'urls': [{
            'url': 'http://t.co/Ech4loAtWx',
            'expanded_url': 'http://youtu.be/9gWNxj5VOhM',
            'display_url': 'youtu.be/9gWNxj5VOhM',
            'indices': [75, 97]
        }],
        'user_mentions': [{
            'screen_name': 'IamPoppCulture',
            'name': 'IamPoppCulture',
            'id': 16525259,
            'id_str': '16525259',
            'indices': [42, 57]
        }, {
            'screen_name': 'YouTube',
            'name': 'YouTube',
            'id': 10228272,
            'id_str': '10228272',
            'indices': [62, 70]
        }],
        'symbols': []
    },
    'favorited': False,
    'retweeted': False,
    'possibly_sensitive': False,
    'filter_level': 'low',
    'lang': 'en',
    'matching_rules': [{
        'tag': None
    }]
}

#mongo_db.insert_tweet_in_collection(db,'suicide',json)
tweets=mongo_db.get_all_tweets_from_collection(db,'tweet_records')

#Permet d'afficher tout les tweets contenus dans la collection

#for i in tweets:
    #print(i)

tweet=mongo_db.get_one_tweet_from_collection(db,'suicide',{"id":461656162237034496})

print(tweet)