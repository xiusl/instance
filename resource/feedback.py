# coding=utf-8
# author:xsl

import hashlib
import datetime
from bson import ObjectId
from flask import g
from flask_restful import reqparse, Resource

from instance.errors import (
    BadRequestError,
    ForbidenError,
    ResourceDoesNotExist,
    MissingRequiredParameter
)
from instance.utils import login_required
from instance.models import User, Feedback


parser = reqparse.RequestParser()
_args = ['content', 'page', 'count', 'contact',
    'replay', 'status']
for _arg in _args:
    parser.add_argument(_arg)

class FeedbacksRes(Resource):

    @login_required
    def post(self):
        args = parser.parse_args()
        content = args.get('content')
        if not content:
            raise MissingRequiredParameter(['content'])
        user_id = g.user_id
        if not user_id:
            raise ForbidenError()
        user = User.objects(id=ObjectId(user_id)).first()
        if not user:
            raise ResourceDoesNotExist()
        
        contact = args.get('contact') or ''

        f = Feedback()
        f.user_id = user_id
        f.content = content
        f.contact = contact
        f.status = Feedback.STATUS_NEED_REPLAY
        f.save()
        return f.pack()

    @login_required
    def get(self):
        user = User.objects(id=ObjectId(g.user_id)).first() 
        if not user:
            raise ForbidenError()
        if user.type != 9:
            raise ForbidenError()

        args = parser.parse_args()
        page = int(args.get('page') or 1)
        count = int(args.get('count') or 10)
        status = args.get('status')
        qs = Feedback.objects().order_by('-created_at')
        if status:
            qs = Feedback.objects(status=int(status or 0)).order_by('-created_at')
        fs = qs.skip(page*count-count).limit(count)
        return {'count':qs.count(), 'data': [f.pack() for f in fs]}


class FeedbackRes(Resource):

    @login_required
    def post(self, id):
        user = User.objects(id=ObjectId(g.user_id)).first()
        if not user or user.type != 9:
            raise ForbidenError()
        # replay feedback
        args = parser.parse_args()
        replay = args.get('replay')
        if not replay:
            raise MissingRequiredParameter(['replay'])
        f = Feedback.objects(id=ObjectId(id)).first()
        if not f:
            raise ResourceDoesNotExist()
        if f.status != Feedback.STATUS_NEED_REPLAY:
            return f.pack()

        f.replay = replay
        f.replay_time = datetime.datetime.now()
        f.status = Feedback.STATUS_FINISHED
        f.save()
        return f.pack()

class UserFeedbackRes(Resource):

    @login_required
    def get(self, id):
        args = parser.parse_args()
        page = int(args.get('page') or 1)
        count = int(args.get('count') or 10)
        
        qs = Feedback.objects(user_id=ObjectId(id)).order_by('-created_at')
        fs = qs.skip(page*count-count).limit(count)
        
        return {'count':qs.count(),'data': [f.pack() for f in fs]}



