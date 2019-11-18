# coding=utf-8
# author:xsl

import pymongo
from bson import ObjectId

def fix_poem():
    db = pymongo.MongoClient('mongodb://127.0.0.1:27017/poem_db')
    au = db['poem_db'].poem_a

    data = au.find()

    for d in data:
        print(d.get('id'))
        idd = d.get('_id')
        au.update_one({'_id': idd},{'$rename':{'id': 'o_id'}})

def fix_rel():
    db = pymongo.MongoClient('mongodb://127.0.0.1:27017/poem_db')
    p_col = db['poem_db'].poem_a
    a_col = db['poem_db'].author_a
    print(a_col)
    f_id = '5dd225268c47d441b6f25c97'
    data = p_col.find({'_id': {'$gt':ObjectId(f_id)}})

    errs = []
    for d in data:
        author  = d.get('author')
        aa = a_col.find_one({'nameStr': author})
        if aa:
            aa_id = aa.get('_id')
            print('{0}: {1}'.format(author, d.get('nameStr')))
            p_col.update_one({'o_id': d.get('o_id')}, {'$set': {'author_id': aa_id}})
        else:
            print('not found')
            ss = '{0}: {1} -> {2}'.format(author, d.get('nameStr'), d.get('_id'))
            print(ss)
            errs.append(ss)
            continue
    print(errs)

def fix_count():
    db = pymongo.MongoClient('mongodb://127.0.0.1:27017/poem_db')
    a_col = db['poem_db'].author_a
    p_col = db['poem_db'].poem_a
    data = a_col.find()
    for d in data:
        idd = d.get('_id')
        c = p_col.count_documents({'author_id': idd})
        a_col.update_one({'_id': idd}, {'$set': {'poems_count': c}})
        print('{0}: {1}'.format(d.get('nameStr'), c))
        


#fix_poem()
#fix_rel()
fix_count()
