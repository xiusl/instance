# coding=utf-8
# author:xsl

import pymongo
from bson import ObjectId

cli = pymongo.MongoClient('mongodb://127.0.0.1:27017/instance_db')

artcol = cli["instance_db"].article

arts = artcol.find()


uID = "5cff6fd1322a5bf8a755471c"


for art in arts:
    idd = art.get('_id')
    artcol.update_one({'_id': idd}, {'$set': {'user_id': ObjectId(uID)}})
