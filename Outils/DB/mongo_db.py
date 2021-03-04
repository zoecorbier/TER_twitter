#conda install pymongo
#Peut-être créer une fichier qui installe toutes les dépendances automatiquement
import sys

import pymongo
from bson.json_util import loads, dumps

import secrets

user=secrets.mongo_name_access
password=secrets.mongo_password

##Database connection

def connection():
    try:
        client=pymongo.MongoClient("mongodb+srv://lucas:9gBYJZuhS7TVGAj6@application.wl73u.mongodb.net/tweet?retryWrites=true&w=majority")
        print('Connexion réussie', client.database_names)
    except:
        print('Problème avec la connexion à la base')
    return client

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
        return db.collection.find_one(information)
    except :
        print("Unexpected error:", sys.exc_info()[0])
    

def bson_json_file(file):
    """
    Convert bson file to json
    return : json file
    """
    try :
        json_str = dumps(file)
        return loads(json_str)
    except :
        print("Unexpected error:", sys.exc_info()[0])



