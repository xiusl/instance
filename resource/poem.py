# coding=utf-8
# author:xsl

from bson import ObjectId
from flask import g
from flask_restful import reqparse, Resource
from instance.models import PoemAuthor, Poem, PoemTag


parser = reqparse.RequestParser()

_args = ['page', 'count', 'author']
for _arg in _args:
    parser.add_argument(_arg)


class PoemAuthorsRes(Resource):

    def get(self):
        args = parser.parse_args()
        page = int(args.get('page') or 1)
        count = int(args.get('count') or 10)
        qs = PoemAuthor.objects()
        total = qs.count()
        data = qs.skip((page-1)*count).limit(count)
        return {'count':total, 'authors': [a.pack() for a in data]}


class PoemsRes(Resource):

    def get(self):
        args = parser.parse_args()
        page = int(args.get('page') or 1)
        count = int(args.get('count') or 10)
        author = args.get('author') or ''
        if len(author) > 0:
            qs = Poem.objects(author=author)
        else:
            qs = Poem.objects()
        total = qs.count()
        data = qs.skip((page-1)*count).limit(count)
        return {'count':total, 'poems': [a.pack() for a in data]}

class PoemTagsRes(Resource):

    def get(self):
        args = parser.parse_args()
        page = int(args.get('page') or 1)
        count = int(args.get('count') or 10)
        qs = PoemTag.objects()
        total = qs.count()
        data = qs.skip((page-1)*count).limit(count)
        return {'count':total, 'tags': [a.pack() for a in data]}
