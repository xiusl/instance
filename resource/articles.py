# coding=utf-8
# author:xsl

import requests
import json
from flask import g, current_app
from flask_restful import reqparse, Resource
from bson import ObjectId
from instance.models import Article, Tag, SpArtSmp, Source
from instance.utils import login_required, query_paging 
from instance.errors import (
    BadRequestError, 
    ResourceDoesNotExist,
    TipMessageError,
    MissingRequiredParameter
)

parser = reqparse.RequestParser()
_args = ['id', 'url', 'page', 'count', 'type',
         'name', 'identifier', 'avatar',
         'level', 'status', 'trans_text',
         'cursor', 'direction', 'title',
         'author', 'spider', 'article']
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
        trans_text = args.get('trans_text')
        if trans_text and len(trans_text) > 0:
            art.transcoding = trans_text
        title = args.get('title')
        if title and len(title) > 0:
            art.title = title
        author = args.get('author')
        if author and len(author) > 0:
            art.author = author
        spider = args.get('spider')
        if spider:
            art.spider = int(spider)
        art.save()
        return art.pack()


class ArticlesRes(Resource):

    def get(self):
        args = parser.parse_args()
        page = args.get('page')
        count = int(args.get('count') or 10)
        cursor = args.get('cursor')
        spider = args.get('spider')
        if cursor and not page:
            direction = int(args.get('direction') or 1)
            qs = Article.objects().filter(status__gte=0)
            arts = query_paging(qs, cursor, direction, count)
            total = qs.count()
            return {"count":total, "articles":[art.pack() for art in arts]}
        page = int(args.get('page') or 1)
        skip = (page - 1)*count
        if spider: # 批量爬取的
            qs = Article.objects(spider=spider).filter(status__get=0).order_by("-created_at")
        else:
            if g.source == 'web':
                qs = Article.objects().filter().order_by("-created_at")
            else:
                qs = Article.objects().filter(status__gte=0).order_by("-created_at")
        arts = list(qs.skip(skip).limit(count))
        total = qs.count()
        return {"count":total, "articles":[art.pack() for art in arts]}


class SpiderArticleRes(Resource):

    def post(self):
        args = parser.parse_args()
        article = args.get('article')
        article = json.loads(article)
        a = Article()
        for key in article.keys():
            setattr(a, key, article.get(key))
        a.save()
        return article


class ArticleSpiderRes(Resource):

    def post(self):
        args = parser.parse_args()
        url = args.get('url')
        session = requests.session()
        headers = {'Content-Type':'application/json'}
        data = {'url': url}
        u = 'http://192.144.171.238/spider'
        if current_app.config['DEBUG']:
            u = 'http://127.0.0.1:5001/spider'
        res = session.post(u, json=data, headers=headers, verify=False)
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


class SpiderArtsRes(Resource):

    def get(self):
        args = parser.parse_args()
        page = int(args.get('page') or 1)
        count = int(args.get('count') or 10)
        skip = (page - 1)*count
        qs = SpArtSmp.objects()
        arts = list(qs.skip(skip).limit(count))
        total = qs.count()
        return {"count":total, "articles":[art.pack() for art in arts]}


class TagsRes(Resource):

    def get(self):
        args = parser.parse_args()
        page = int(args.get('page') or 1)
        count = int(args.get('count') or 10)

        skip = (page - 1)*count
        qs = Tag.objects()
        tags = list(qs.skip(skip).limit(count))
        total = qs.count()
        return {'count': total, 'tags': [tag.pack() for tag in tags]}

    @login_required
    def post(self):
        args = parser.parse_args()
        name = args.get('name')

        tag = Tag()
        tag.name = name
        tag.user_id = g.user_id
        tag.save()

        return tag.pack()

class TagRes(Resource):

    def get(self, id):
        tag = Tag.objects(id=ObjectId(id)).first()

        return tag.pack()

    @login_required
    def delete(self, id):
        tag = Tag.objects(id=ObjectId(id)).first()

        if not tag:
            raise ResourceDoesNotExist()

        tag.delete()
        
        return tag.pack()


class ArticleTagsRes(Resource):

    @login_required
    def post(self, id):
        art = Article.objects(id=ObjectId(id)).first()

        if not art:
            raise ResourceDoesNotExist()

        args = parser.parse_args()

        name = args.get('name')

        art.tag = name
        art.save()

        return art.pack(g_user=g.user_id)
