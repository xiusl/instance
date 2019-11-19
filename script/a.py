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
        

def fix_tag():
    db = pymongo.MongoClient('mongodb://127.0.0.1:27017/poem_db')
    p_col = db['poem_db'].poem_a
    data = p_col.find()
    t_col = db['poem_db'].tag_a
    for d in data:
        tags = d.get('tag').split('|')
        for t in tags:
            ot = t_col.find_one({'name': t})
            if ot:
                print('exsit: {0}'.format(t))
                continue
            t_col.insert_one({'name': t})

    print('tag count: {0}'.format(t_col.counts))

fx = ['早教','唐诗三百首', '小学古诗', '小学生必背古诗70首', '小学生必背古诗80首', 
        '初中古诗', '高中古诗', '宋词三百首', '宋词精选', '初中文言文',
        '古诗三百首', '高中文言文', '小学文言文', '山水小学生必背古诗70首', '生活小学生必背古诗80首',
        '山水小学生必背古诗70首', '抒情小学生必背古诗70首', '早教小学生必背古诗70首',]
def fix_tag2():
    db = pymongo.MongoClient('mongodb://127.0.0.1:27017/poem_db')
    p_col = db['poem_db'].poem_a
    data = p_col.find()
    for d in data:
        tags = d.get('tag').split('|')
        cs = []
        ocs = d.get('collection') or ''
        if len(ocs):
            ocs = ocs.split('|')
            cs.extend(ocs)
        ts = []
        for t in tags:
            if t in fx:
                cs.append(t)
            else:
                ts.append(t)
        idd = d.get('_id')
        tss = '|'.join(ts)
        css = '|'.join(cs)
        print(css)
        p_col.update_one({'_id': idd}, {'$set': {'tag':tss, 'collection':css}})

#fix_poem()
#fix_rel()
#fix_count()
fix_tag2()
