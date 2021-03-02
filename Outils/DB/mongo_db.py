#conda install pymongo
#Peut-être créer une fichier qui installe toutes les dépendances automatiquement

import pymongo
import secrets

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
    return client

def insert_tweet(db,collection,tweet):
    """
    db : MongoClient Object
    collection : collection dans la base, équivalent aux tables dans sql
    tweet : fichier tweet au format json provenant directement de l'API
    return : nothing
    """
    try :
        return db.collection.insert_one(tweet)
    except :
        print('Error during',EOFError)

def get_all_tweets_from_collection(db,collection):
    """
    Permet de récupérer les tweets provenant d'une collection
    """
    try :
        return db.collection
    except :
        print('Error during',EOFError)
    
def get_one_tweet_from_collection(db,collection,objets):
    """
    Permet de récupérer un tweet avec un objet type json 
    """
    try :
        return db.collection.find(objets)
    except :
        print('Error during', EOFError)
