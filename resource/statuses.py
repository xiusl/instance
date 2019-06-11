# coding=utf-8
# author:xsl

import datetime
from bson import ObjectId
from flask import g
from flask_restful import reqparse, fields, marshal_with, Resource
from instance.errors import BadRequestError, ResourceDoesNotExist, MissingRequiredParameter
from instance.utils import login_required
from instance.models import User, Status

parser = reqparse.RequestParser()

_args = ['id', 'page', 'cursor', 'director', 'count',
        'content', ]
for arg in _args:
    parser.add_argument(arg)

parser.add_argument('images', type=dict, action='append')



class StatusesRes(Resource):


    def get(self):
        args = parser.parse_args()
        count = 10
        page = 1
        page -= page
        ss = Status.objects.skip(page*count).limit(count)
        return list([s.pack() for s in ss])


    @login_required
    def post(self):
        args = parser.parse_args()
        content = args.get('content')
        images = args.get('images')
        print(images)
        print(type(images))
        for im in images:
            print(im)
            print(type(im))
        user = g.user
        if not content:
            raise MissingRequiredParameter(['content'])
        s = Status()
        s.content = content
        s.images = images
        s.user_id = user.id
        s.save()
        return s.pack() 

class StatusRes(Resource):

    def get(self, id):
        if not id:
            raise MissingRequiredParameter(['id'])
        s = Status.objects(id=ObjectId(id)).first()
        if not s:
            raise ResourceDoesNotExist()
        return s.pack()
