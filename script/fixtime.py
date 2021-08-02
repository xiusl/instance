# coding=utf-8
# author:xsl

import pymongo
import datetime

cli = pymongo.MongoClient('mongodb://127.0.0.1:27017/instance_db')

artcol = cli["instance_db"].article

arts = artcol.find()

for art in arts:
    idd = art.get('_id')
    t1 = art['created_at']
    ct = t1.ctime()

    dd = datetime.datetime.strptime(ct, '%a %b %d %H:%M:%S %Y')

    artcol.update_one({'_id': idd}, {'$set': {'created_at': dd}})
    break
