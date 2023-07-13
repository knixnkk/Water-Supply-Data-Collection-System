import pymongo
from pymongo import MongoClient
import os
import datetime
import uuid
user = os.environ.get("DB_USER")
secret = os.environ.get("DB_PASS")

cluster = pymongo.MongoClient(f"mongodb://localhost:27017")
db = cluster["local"]
collection = db["UnitWithHouseAddr"]
def timenow():
    mydate = datetime.datetime.now()
    timenow = (mydate.strftime("%X"))
    return timenow
def calPrice(unit):
    price = 0
    for i in range(1,int(unit)+1):
        if i >= 0 and i <= 10:
            price += 10.20
        elif i > 10 and i <= 20:
            price += 16.00
        elif i > 20 and i <= 30:
            price += 19.00
        elif i > 30 and i <= 50:
            price += 21.20
        elif i > 50 and i <= 80:
            price += 21.60
        elif i >80 and i <= 100:
            price += 21.65
        elif i > 100 and i <= 300:
            price += 21.70
        elif i > 300 and i <= 1000:
            price += 21.75
        elif i > 1000 and i <= 2000:
            price += 21.80
        elif i > 2000 and i <= 3000:
            price += 21.85
        elif i > 3000:
            price += 21.90
    return int(price)
def getData(string):
    collections = collection.find()
    for item in collections:
        if item['Username'] == str(string):
            return item['Username'], item["Password"], item["telephone"], item["Addr"], item['Unit'], item["time"]
def check_for_user(string):
    if collection.find_one({"Username" : string}):
        return True
    else:
        return False
def get_user(string):
    return collection.find_one({"Username" : string})

def updateUnit(string, new_unit):
    _,_,_,_,old_unit,_ = getData(string)
    if int(float(old_unit)) != int(float(old_unit))+int(float(new_unit)):
        query = {'Username': string}
        update = {'$set': {'Unit': int(float(old_unit))+int(float(new_unit)), 'time':timenow(), 'Price': str(calPrice(int(float(old_unit))+int(float(new_unit))))}}
        collection.update_one(query, update)
    else:
        print('Same')
def getAllData():
    data = []
    collections = collection.find()
    for item in collections:
        data.append((item["HouseNo"],item["Name"], item["Unit"], item["Price"], str(round(int(item["Price"])*0.07, 2)), str(int(item["Price"]) + (int(item["Price"])*0.07))))
    return data
def getDashboard(string):
    collections = collection.find()
    for item in collections:
        if item['Username'] == str(string):
            return item['Addr'], item["Unit"], item["Price"], item["time"], item['Name']
# def delete_user(user):
#     pass
    
# def update_user(user):
    
