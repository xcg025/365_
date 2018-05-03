import pymongo as pm
from pymongo import MongoClient

client = MongoClient("mongodb://ajmd:ajmd123@123.206.8.19:27017/bet365")
db = client['bet365']
datas = db['collections'].find()
for data in datas:
    print(data.get('_parties_name'))