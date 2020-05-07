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
from instance.models import User, Status, UserAction

parser = reqparse.RequestParser()

_args = ['id', 'page', 'cursor', 'director', 'count',
        'content',]
for arg in _args:
    parser.add_argument(arg)

parser.add_argument('images', type=dict, action='append')



class StatusesRes(Resource):


    def get(self):
        args = parser.parse_args()
        page = int(args.get('page') or 1)
        page = page if page > 0 else 1
        count = int(args.get('count') or 10)
        skip = (page-1)*count
        qs = Status.objects().filter(status__ne=-2)
        ss = qs.skip(skip).limit(count).order_by('-created_at')
        return {'count':qs.count(), 'statuses': list([s.pack(user_id=g.user_id) for s in ss])}


    @login_required
    def post(self):
        args = parser.parse_args()
        content = args.get('content')
        images = args.get('images') or []
        user = g.user
        if not content:
            raise MissingRequiredParameter(['content'])
        s = Status(content=content,images=images)
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
        s.status = -2
        s.save()
        return {"msg": "Delete Success"}

class UserStatusesRes(Resource):

    def get(self, user_id):
        args = parser.parse_args()
        page = int(args.get('page') or 1)
        count = int(args.get('count') or 10)
        if not user_id:
            raise MissingRequiredParameter(['user_id'])
        ss = Status.objects(user_id=user_id).filter(status__ne=-2).skip(page*count-count).limit(count).order_by('-created_at')
        return [s.pack(g.user_id) for s in ss if s]


class StatusLikesRes(Resource):

    def get(self, id):
        if not id:
            raise MissingRequiredParameter(['id'])
        s = Status.objects(id=ObjectId(id)).first()
        if not s:
            raise ResourceDoesNotExist()
        rels = UserAction.objects(status_id=s.id, action=UserAction.ACTION_LIKE).skip(0).limit(10)
        uis = list([rel.user_id for rel in rels])
        us = list([User.objects(id=ObjectId(u_id)).first().pack(user_id=g.user_id) for u_id in uis])
        return us

    @login_required
    def post(self, id):
        if not id:
            raise MissingRequiredParameter(['id'])
        s = Status.objects(id=ObjectId(id)).first()
        if not s:
            raise ResourceDoesNotExist()
        if s.is_liked(g.user_id):
            return {"msg": "did liked"}
        r = UserAction(status_id=s.id, user_id=g.user_id, action=UserAction.ACTION_LIKE)
        r.save()
        s.like_count += 1
        s.save()
        return s.pack(user_id=g.user_id)


    @login_required
    def delete(self, id):
        if not id:
            raise MissingRequiredParameter(['id'])
        s = Status.objects(id=ObjectId(id)).first()
        if not s:
            raise ResourceDoesNotExist()
        if not s.is_liked(g.user_id):
            return {"msg": "unlike faliure"}
        r = UserAction.objects(status_id=s.id, user_id=g.user_id, action=UserAction.ACTION_LIKE)
        r.delete()
        s.like_count -= 1
        s.save()
        return s.pack(user_id=g.user_id)

