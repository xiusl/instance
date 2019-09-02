# coding=utf-8
# author:xsl

import requests
from flask import g
from flask_restful import reqparse, Resource
from bson import ObjectId
from instance.models import Article, Source
from instance.errors import (
    BadRequestError, 
    ResourceDoesNotExist,
    MissingRequiredParameter
)

parser = reqparse.RequestParser()
_args = ['id', 'url', 'page', 'count', 'type',
         'name', 'identifier', 'avatar',
         'level', 'status']
for _arg in _args:
    parser.add_argument(_arg)

class ArticleRes(Resource):

    def get(self, id):
        art = Article.objects(id=ObjectId(id)).first()
        if not art:
            raise ResourceDoesNotExist
        return art.pack()

    def delete(self, id):
        art = Article.objects(id=ObjectId(id)).first()
        if not art:
            raise ResourceDoesNotExist
        art.status = -2
        art.save()
        return art.pack()

class ArticlesRes(Resource):

    def get(self):
        args = parser.parse_args()
        page = int(args.get('page')) or 1
        count = int(args.get('count')) or 10
        skip = (page - 1)*count
        qs = Article.objects().filter(status__ne=-2)
        arts = qs.skip(skip).limit(count)
        total = qs.count()
        return {"count":total, "articles":list([art.pack() for art in arts])}

class ArticleSpiderRes(Resource):

    def post(self):
        args = parser.parse_args()
        url = args.get('url')
        type = args.get('type')
        session = requests.session()
        headers = {'Content-Type':'application/json'}
        data = {'url': url}
        res = session.post('http://127.0.0.1:5001/'+type, json=data, headers=headers, verify=False)
        return {'ok':1}


    def get(self):
        args = parser.parse_args()
        url = args.get('url')
        art = Article.objects(original_url=url).first()
        if not art:
            raise ResourceDoesNotExist()

        return art.pack()

class SourcesRes(Resource):

    def get(self):
        pass

    def post(self):
        args = parser.parse_args()
        name = args.get('name')
        ident = args.get('identifier')
        spider_url = args.get('url')
        if not name or not ident or not spider_url:
            raise MissingRequiredParameter(['name', '...']) 
        avatar = args.get('avatar')
        type = args.get('type')
        s = Source(name=name, ident=ident, spider_url=spider_url)
        s.avatar = avatar
        s.type = type
        s.save()
        return s.pack()
         
