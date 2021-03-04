#conda install pymongo
#Peut-être créer une fichier qui installe toutes les dépendances automatiquement

import pymongo
import secrets
import bson.json_util
import json

user=secrets.mongo_name_access
password=secrets.mongo_password

def connection(base):
    """
    Créer une connexion à la base de données spécifiée
    return :
        MongoClient Object : Objet base de données
    """
    try:
        client=pymongo.MongoClient("mongodb+srv://"+user+":"+password+"@application.wl73u.mongodb.net/"+base+"?retryWrites=true&w=majority")
        print('Connexion réussie à la base : ',base)
    except:
        print('Problème avec la connexion à la base')
    return client[base]

def insert_tweet_in_collection(db,collection,tweet):
    """
    db : MongoClient Object
    collection : collection dans la base, équivalent aux tables dans sql
    tweet : fichier tweet au format json provenant directement de l'API
    return : nothing
    """
    try :
        db[collection].insert_one(tweet)
        print('Insertion terminée')
    except :
        print('Error during',EnvironmentError)

def get_all_tweets_from_collection(db,collection):
    """
    Permet de récupérer les tweets provenant d'une collection
    Return :
        Objet contenant l'ensemble des tweets d'une collection
    """
    try :
        return db[collection].find()
    except :
        print('Error during',EOFError)
    
def get_one_tweet_from_collection(db,collection,objets):
    """
    Permet de récupérer un tweet avec un objet type json 
    """
    try :
        return db.collection.find_one(objets)
    except :
        print('Error during', EOFError)

def bson_json_file(file):
    """
    Convert bson file to json
    return : json file
    """
    try :
        file_dumped = bson.json_util.dumps(file)
        return json.loads(file_dumped)
    except :
        print("Conversion bson to json have problem")



