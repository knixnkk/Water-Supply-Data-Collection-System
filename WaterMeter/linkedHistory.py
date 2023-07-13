import pymongo
from pymongo import MongoClient
import os
import datetime
import uuid
user = os.environ.get("DB_USER")
secret = os.environ.get("DB_PASS")

cluster = pymongo.MongoClient(f"mongodb://localhost:27017")
db = cluster["local"]
collection = db["History"]
def timenow():
    mydate = datetime.datetime.now()
    timenow = (mydate.strftime("%X"))
    return timenow
def updateHistory(string, unitCount, unit, timenow):
    query = {'Username': string}
    new_values = {'$set': {unitCount: f'{unit}:{timenow}'}}
    collection.update_one(query, new_values)
# def delete_user(user):
#     pass
    
# def update_user(user):
    
