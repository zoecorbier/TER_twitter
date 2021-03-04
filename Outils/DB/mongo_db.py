#conda install pymongo
#Peut-être créer une fichier qui installe toutes les dépendances automatiquement
import sys

import pymongo
from bson.json_util import loads, dumps
import json

import secrets

user=secrets.mongo_name_access
password=secrets.mongo_password

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
    if not db.users.find_one({'id':user_info['id']}):
        db.users.insert_one(user_info)
    json['user_id']=user_info['id']
    json['critic_word']=word
    db.tweets.insert_one(json)

if __name__ == "__main__":
    tweet=connection().tweet
    print('Connexion')
    all_tweets=bson_to_json_file(get_all_files_from_collection(tweet,'suicide'))
    print(all_tweets[0])
    create_collection_name(tweet,'suicide','04_03_2020')
