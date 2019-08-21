# coding=utf-8
# author:xsl

import requests
from flask import g
from flask_restful import reqparse, Resource
from instance.models import Article
from instance.errors import BadRequestError, ResourceDoesNotExist

parser = reqparse.RequestParser()
_args = ['url', 'page', 'count']
for _arg in _args:
    parser.add_argument(_arg)

class ArticlesRes(Resource):

    def get(self):
        args = parser.parse_args()
        page = int(args.get('page')) or 1
        count = int(args.get('count')) or 10
        skip = (page - 1)*count
        arts = Article.objects().skip(skip).limit(count)
        total = Article.objects().count()
        return {"count":total, "articles":list([art.pack() for art in arts])}

class ArticleSpiderRes(Resource):

    def post(self):
        args = parser.parse_args()
        url = args.get('url')
        session = requests.session()
        headers = {'Content-Type':'application/json'}
        data = {'url': url}
        print(data)
        res = session.post('http://127.0.0.1:5001/weibo', json=data, headers=headers, verify=False)
        print(res.text)
        return {'ok':1}


    def get(self):
        args = parser.parse_args()
        url = args.get('url')
        art = Article.objects(original_url=url).first()
        if not art:
            raise ResourceDoesNotExist()

        return art.pack()
