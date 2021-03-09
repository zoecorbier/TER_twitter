#conda install pymongo
#Peut-être créer une fichier qui installe toutes les dépendances automatiquement
import sys

import pymongo
from bson.json_util import loads, dumps
import json

import secrets

user=secrets.mongo_name_access
password=secrets.mongo_password

print(user)
print(password)

##Database connection

def connection(base='tweet'):
    try:
        client=pymongo.MongoClient("mongodb+srv://"+user+":"+password+"@application.wl73u.mongodb.net/"+base+"?retryWrites=true&w=majority")
        print('Connexion réussie', client.database_names)
    except:
        print("Unexpected error:", sys.exc_info()[0])
    return client

def create_collection_name(db,word,date):
    """
    db : MongoDB object allow database connexion.
    word : terme searched in Twitter API.
    date : witch periode is collected 24_01_2010.
    RETURN :
        string
    """
    if type(word)==str and type(date)==str:
        if len(date) != 10 :
            print('Incorect length for date in collection_name')
        else :
            value=word+'_'+date
            db.create_collection(value)
            print(value,'is created')
    else :
        print('Type error in collection_name')
    
#Database data interaction

def insert_tweet_in_collection(db,collection,file):
    """
    db : MongoClient Object
    collection : collection dans la base, équivalent aux tables dans sql
    tweet : fichier tweet au format json provenant directement de l'API
    return : nothing
    """
    try :
        db[collection].insert_one(file)
        print('Insertion terminée')
    except :
        print("Problème d'insertion")

def get_all_files_from_collection(db,collection):
    """
    Permet de récupérer les tweets provenant d'une collection
    Return :
        Objet contenant l'ensemble des tweets d'une collection
    """
    try :
        return db[collection].find()
    except :
        print("Unexpected error:", sys.exc_info()[0])
    
def get_one_file_from_collection(db,collection,information):
    """
    Permet de récupérer un tweet avec un objet type json 
    """
    try :
        return db[collection].find_one(information)
    except :
        print("Unexpected error:", sys.exc_info()[0])
    
#Fix the bson file

def bson_to_json_file(file):
    """
    Convert bson file to json
    return : json file
    """
    try :
        json_str = dumps(file)
        return loads(json_str)
    except :
        print("Unexpected error:", sys.exc_info()[0])

def json_tweet_model(db,file,word):
    json=bson_to_json_file(file)
    user_info=file['user']
    del json['user']
    if not db["users"].find_one({'id':user_info['id']}):
        db.users.insert_one(user_info)
    json['user_id']=user_info['id']
    json['critic_word']=word
    db.tweets.insert_one(json)

if __name__ == "__main__":
    tweet = connection().tweet
    print('Connexion')
    # all_tweets=bson_to_json_file(get_all_files_from_collection(tweet,'suicide'))
    # print(all_tweets[0])
    # create_collection_name(tweet,'suicide','04_03_2020')
    filen =     {
        "created_at": "Thu Dec 17 19:43:44 +0000 2020",
        "id": 1339657551118360579,
        "id_str": "1339657551118360579",
        "full_text": "@WarrenDuffit @janeteaches79 @l11097458308 @CNN Once again love, Covid is the real cause. Your Dad was obese but because Covid attacked his body at the micro level, he was unable to fight it off. He'd be alive had he not contracted tbe virus..make sense?",
        "display_text_range": [
            48,
            254
        ],
        "entities": {
            "hashtags": [],
            "symbols": [],
            "user_mentions": [
                {
                    "screen_name": "WarrenDuffit",
                    "name": "Warren Duffit",
                    "id": 1275659342994440196,
                    "id_str": "1275659342994440196",
                    "indices": [
                        0,
                        13
                    ]
                },
                {
                    "screen_name": "janeteaches79",
                    "name": "janet eaches",
                    "id": 279619898,
                    "id_str": "279619898",
                    "indices": [
                        14,
                        28
                    ]
                },
                {
                    "screen_name": "l11097458308",
                    "name": "יוגי",
                    "id": 20878320,
                    "id_str": "20878320",
                    "indices": [
                        29,
                        42
                    ]
                },
                {
                    "screen_name": "CNN",
                    "name": "CNN",
                    "id": 759251,
                    "id_str": "759251",
                    "indices": [
                        43,
                        47
                    ]
                }
            ],
            "urls": []
        },
        "metadata": {
            "iso_language_code": "en",
            "result_type": "recent"
        },
        "source": "<a href=\"http://twitter.com/download/android\" rel=\"nofollow\">Twitter for Android</a>",
        "in_reply_to_status_id": 1339641075649134595,
        "in_reply_to_status_id_str": "1339641075649134595",
        "in_reply_to_user_id": 1275659342994440196,
        "in_reply_to_user_id_str": "1275659342994440196",
        "in_reply_to_screen_name": "WarrenDuffit",
        "user": {
            "id": 3245443188,
            "id_str": "3245443188",
            "name": "M'leez Can't Wait for January 20, 2021",
            "screen_name": "realmleez",
            "location": "Las Vegas, NV",
            "description": "Old flower child/hippy current uber liberal I can't believe what #45 is doing to USA! Voting for BIDEN/HARRIS. 🌊🌊🌊🌊 #BLACKLIVESMATTER\nNO DMs PLS!",
            "entities": {
                "description": {
                    "urls": []
                }
            },
    
            "profile_background_color": "C0DEED",
            "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
            "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
 
            "translator_type": "none"
        },

        "place": {
            "id": "009d3c3d41dbb00e",
            "url": "https://api.twitter.com/1.1/geo/id/009d3c3d41dbb00e.json",
            "place_type": "city",
            "name": "Enterprise",
            "full_name": "Enterprise, NV",
            "country_code": "US",
            "country": "United States",
            "contained_within": [],
            "bounding_box": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -115.316075,
                            35.9607531
                        ],
                        [
                            -115.152796,
                            35.9607531
                        ],
                        [
                            -115.152796,
                            36.0768564
                        ],
                        [
                            -115.316075,
                            36.0768564
                        ]
                    ]
                ]
            },
            "attributes": {}
        },

        "lang": "en"
    }
    
    json_tweet_model(tweet, filen, "dad fight")
