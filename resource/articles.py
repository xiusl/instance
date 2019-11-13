# coding=utf-8
# author:xsl

import requests
from flask import g
from flask_restful import reqparse, Resource
from bson import ObjectId
from instance.models import Article, Source
from instance.utils import login_required
from instance.errors import (
    BadRequestError, 
    ResourceDoesNotExist,
    TipMessageError,
    MissingRequiredParameter
)

parser = reqparse.RequestParser()
_args = ['id', 'url', 'page', 'count', 'type',
         'name', 'identifier', 'avatar',
         'level', 'status', 'trans_text']
for _arg in _args:
    parser.add_argument(_arg)

class ArticleRes(Resource):

    def get(self, id):
        art = Article.objects(id=ObjectId(id)).first()
        if not art:
            raise ResourceDoesNotExist
        return art.pack(trans=True)

    @login_required
    def delete(self, id):
        art = Article.objects(id=ObjectId(id)).first()
        if not art:
            raise ResourceDoesNotExist
        art.status = -2
        art.save()
        return art.pack()

    @login_required
    def patch(self, id):
        art = Article.objects(id=ObjectId(id)).first()
        if not art:
            raise ResourceDoesNotExist
        args = parser.parse_args()
        trans_text = args.get('trans_text') or ''
        if len(trans_text) <= 0:
            raise TipMessageError('content len == 0')
        art.transcoding = trans_text
        art.save()
        return art.pack()


class ArticlesRes(Resource):

    def get(self):
        args = parser.parse_args()
        page = int(args.get('page') or 1)
        count = int(args.get('count') or 10)
        skip = (page - 1)*count
        qs = Article.objects().filter(status__ne=-2).order_by("-created_at")
        arts = list(qs.skip(skip).limit(count))
        total = qs.count()
        return {"count":total, "articles":[art.pack() for art in arts]}


class ArticleSpiderRes(Resource):

    def post(self):
        args = parser.parse_args()
        url = args.get('url')
        type = args.get('type')
        session = requests.session()
        headers = {'Content-Type':'application/json'}
        data = {'url': url}

        if type == None:
            if '36kr' in url:
                type = 'kr36'
            elif 'weibo' in url:
                type = 'weibo'
            elif 'weixin' in url:
                type = 'wechat'
            elif 'laohu' in url:
                type = 'laohu'
            elif 'jianshu' in url:
                type = 'jianshu'
            else:
                type  = ''

        res = session.post('http://149.129.97.184/'+type, json=data, headers=headers, verify=False)
        #res = session.post('http://127.0.0.1:5001/'+type, json=data, headers=headers, verify=False)
        return {'ok':1}


    def get(self):
        args = parser.parse_args()
        url = args.get('url')
        art = Article.objects(original_url=url).first()
        if not art:
            raise ResourceDoesNotExist()

        return art.pack()

class SourceRes(Resource):
    def get(self):
        pass

    def post(self):
        pass

class SourcesRes(Resource):

    def get(self):
        args = parser.parse_args()
        page = int(args.get('page') or 1)
        count = int(args.get('count') or 10)
        skip = (page - 1)*count
        qs = Source.objects().filter(status__ne=-2).order_by("-created_at")
        arts = list(qs.skip(skip).limit(count))
        total = qs.count()
        return {"count":total, "sources":[art.pack() for art in arts]}



    def post(self):
        args = parser.parse_args()
        name = args.get('name')
        url = args.get('url')
        spider_url = args.get('url')
        if not name or not spider_url:
            raise MissingRequiredParameter(['name', '...']) 
        avatar = args.get('avatar')
        type = args.get('type')
        s = Source(name=name, spider_url=spider_url)
        s.avatar = avatar
        s.url = url
        s.type = type
        s.save()
        return s.pack()
         
