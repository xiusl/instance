# coding=utf-8
# author:xsl

import requests
from flask import g
from flask_restful import reqparse, Resource
from instance.models import Article
from instance.errors import BadRequestError, ResourceDoesNotExist

parser = reqparse.RequestParser()
_args = ['id', 'url', 'page', 'count', 'type']
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
