import Outils.data_extraction.mongo_db as mg
import pymongo

db=mg.connection()

base_de_donnees=db.address
print(base_de_donnees)

#print(db.tweets.find_one({"user_id":"1192378724097961985"}))
tweet = mg.connection().tweet
mg.bson_to_json_file(mg.get_all_files_from_collection(tweet,"tweets"))
