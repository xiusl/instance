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
from instance.models import (
    UserTopicRef, User, Status, UserAction, Topic,
    StatusAt, StatusTopicRef
)

parser = reqparse.RequestParser()

_args = ['id', 'page', 'cursor', 'director', 'count',
        'content', 'name', 'desc', 'logo',
        'topic_id','topic']
for arg in _args:
    parser.add_argument(arg)

parser.add_argument('images', type=dict, action='append')



class StatusesRes(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.config_reqparse()
        super(StatusesRes, self).__init__()

    def config_reqparse(self):
        _args = ['id', 'page', 'cursor', 'director', 
        'count', 'content', 'name', 'desc', 
        'logo', 'topic_id','topic', 'visible']
        for arg in _args:
            self.reqparse.add_argument(arg)
        self.reqparse.add_argument('images', type=dict, action='append')
        self.reqparse.add_argument('location', type=dict)
        self.reqparse.add_argument('at', type=dict, action='append')
        self.reqparse.add_argument('topics', type=dict, action='append')


    def get(self):
        args = self.reqparser.parse_args()
        page = int(args.get('page') or 1)
        page = page if page > 0 else 1
        count = int(args.get('count') or 10)
        skip = (page-1)*count

        status_ids = []
        if g.user_id:
            rels = UserAction.objects(user_id=g.user_id, action=UserAction.ACTION_SHIELD)
            status_ids = list([rel.status_id for rel in rels])

        if g.source == 'web':
            qs = Status.objects()
        else:
            qs = Status.objects().filter(status__gte=0, id__not__in=status_ids)

        ss = qs.skip(skip).limit(count).order_by('-created_at')
        return {'count':qs.count(), 'statuses': list([s.pack(user_id=g.user_id) for s in ss])}


    # @login_required
    def post(self):
        args = self.reqparse.parse_args()
        content = args.get('content')
        images = args.get('images') or []
        topic = args.get('topic')
        location = args.get('location')
        visible = args.get('visible') or 0
        at = args.get('at') or []
        topics = args.get('topics') or []
        print(location)
        user = g.user
        if not content:
            raise MissingRequiredParameter(['content'])
        s = Status(content=content,images=images,location=location, visible=visible)
        s.user_id = user.id
        if ObjectId.is_valid(topic):
            s.topic_id = ObjectId(topic)

        s.save()

        for u in at:
            # 异步通知被人@
            print("动态 {} @ {}".format(s.id, u.get("name")))
        if len(at) > 0:
            a = StatusAt(status_id=s.id, users=at)
            a.save()
        
        if len(topics) > 0:
            for topic in topics:
                topic_id = topic.get('id')
                topic_name = topic.get('name')
                t = Topic.objects.get_any(topic_id, topic_name)
                if not t:
                    t = Topic(name=topic.get('name'))
                    t.save()
                st = StatusTopicRef(status_id=s.id, topic_id=t.id)
                st.save()
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
        ss = Status.objects(user_id=user_id).filter(status__gte=0).skip(page*count-count).limit(count).order_by('-created_at')
        return [s.pack(g.user_id) for s in ss if s]

class StatusShieldsRes(Resource):
    
    @login_required
    def post(self, id):
        if not id:
            raise MissingRequiredParameter['id']
        s = Status.objects(id=ObjectId(id)).first()
        if not s:
            raise ResourceDoesNotExist()

        user_act = UserAction(status_id=s.id, user_id=g.user_id, action=UserAction.ACTION_SHIELD)
        user_act.save()
        return s.pack(user_id=g.user_id)

    @login_required
    def delete(self, id):
        if not id:
            raise MissingRequiredParameter['id']
        s = Status.objects(id=ObjectId(id)).first()
        if not s:
            raise ResourceDoesNotExist()
        r = UserAction.objects(status_id=s.id, user_id=g.user_id, action=UserAction.ACTION_SHIELD)
        r.delete()
        return s.pack(user_id=g.user_id)


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
        r = UserAction(status_id=s.id, 
                user_id=g.user_id, 
                action=UserAction.ACTION_LIKE)
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
        r = UserAction.objects(status_id=s.id, 
                user_id=g.user_id, 
                action=UserAction.ACTION_LIKE)
        r.delete()
        s.like_count -= 1
        s.save()
        return s.pack(user_id=g.user_id)

class TopicsRes(Resource):

    def get(self):
        args = parser.parse_args()
        page = int(args.get('page') or 1)
        count = int(args.get('count') or 10)

        qs = Topic.objects()
        tps = qs.skip(page*count-count).limit(count)
        
        return {'count': qs.count(), 
            'topics': [t.pack(user_id=g.user_id) for t in tps]}

    @login_required
    def post(self):
        args = parser.parse_args()
        name = args.get('name')
        if not name or len(str(name)) == 0:
            raise MissingRequiredParameter(['name'])
        logo = args.get('logo')
        desc = args.get('desc')

        t = Topic.objects(name=name).first()
        if t:
            return t.pack()
        t = Topic()
        t.name = name
        t.logo = logo
        t.desc = desc
        t.user_id = g.user_id
        t.save()

        return t.pack(user_id=g.user_id)


class TopicStatusesRes(Resource):

    def get(self, id):
        args = parser.parse_args()
        page = int(args.get('page') or 1)
        count = int(args.get('count') or 10)

        qs = Status.objects(topic_id=id)\
                .filter(status__gte=0).order_by('-created_at')

        ss = qs.skip(page*count-count).limit(count)
        
        return {'count': qs.count(), 
                'statuses': [s.pack(user_id=g.user_id) for s in ss]}


class TopicUsersRes(Resource):
    # /topics/<id>/users

    def get(self, id):
        # get users of topic
        args = parser.parse_args()
        page = int(args.get('page') or 1)
        count = int(args.get('count') or 10)

        rels = UserTopicRef.objects(topic_id=id,
                action=UserTopicRef.JOIN)\
                    .order_by('-created_at')
        qs = rels.skip(page*count-count).limit(count)
        uids = [rel.user_id for rel in qs]

        users = User.objects().filter(id__in=uids)
        return [u.pack(user_id=g.user_id) for u in users]

    @login_required
    def post(self, id):
        t = Topic.objects(id=ObjectId(id)).first()
        if not t:
            raise ResourceDoesNotExist()
        ref = UserTopicRef.objects(topic_id=id,
                user_id=g.user_id).first()
        if ref:
            return t.pack()
        ref = UserTopicRef()
        ref.topic_id = id
        ref.user_id = g.user_id
        ref.action = UserTopicRef.JOIN
        ref.save()

        t.joined_count += 1
        t.save()
        return t.pack(user_id=g.user_id)

    @login_required
    def delete(self, id):
        t = Topic.objects(id=ObjectId(id)).first()
        if not t:
            raise ResourceDoesNotExist()
        ref = UserTopicRef.objects(topic_id=id,
                user_id=g.user_id).first()
        if ref:
            t.joined_count -= 1
            t.save()
            ref.delete()
        
        return t.pack(user_id=g.user_id)
