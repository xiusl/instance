# coding=utf-8
# author:xsl

import datetime
from bson import ObjectId
from flask import g
from flask_restful import reqparse, fields, marshal_with, Resource
from instance.errors import (
    BadRequestError, 
    ResourceDoesNotExist, 
    MissingRequiredParameter,
    OperationForbiddenError
)
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
        return list([s.pack(user_id=g.user_id) for s in ss])


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

    @login_required
    def post(self, id):
        if not id:
            raise MissingRequiredParameter(['id'])
        s = Status.objects(id=ObjectId(id)).first()
        if not s:
            raise ResourceDoesNotExist()
        if str(s.user_id) != str(g.user_id) and not g.user.is_admin:
            raise OperationForbiddenError()
        args = parser.parse_args()
        content = args.get('content')
        if not content:
            raise MissingRequiredParameter(['content'])
        images = args.get('images')
        if images:
            s.images = images
        s.content = content
        s.updated_at = datetime.datetime.now()
        s.save()
        return s.pack(user_id=g.user_id)

    @login_required
    def delete(self, id):
        if not id:
            raise MissingRequiredParameter(['id'])
        s = Status.objects(id=ObjectId(id)).first()
        if not s:
            raise ResourceDoesNotExist()
        print(g.user.is_admin)
        if str(s.user_id) != str(g.user_id) and not g.user.is_admin:
            raise OperationForbiddenError()
        s.delete()
        return {"msg": "Delete Success"}

class UserStatusesRes(Resource):

    def get(self, user_id):
        if not user_id:
            raise MissingRequiredParameter(['user_id'])
        ss = Status.objects(user_id=user_id).skip(0).limit(10)
        return [s.pack(g.user_id) for s in ss]




