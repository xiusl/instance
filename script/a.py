# coding=utf-8
# author:xsl


import pymongo

db = pymongo.MongoClient('mongodb://127.0.0.1:27017/poem_db')
au = db['poem_db'].poem_a

data = au.find()

for d in data:
    print(d.get('id'))
    idd = d.get('_id')
    au.update_one({'_id': idd},{'$rename':{'id': 'o_id'}})
