# coding=utf-8
# author:xsl

from mongoengine import (
    Document,
    DynamicDocument,
    ObjectIdField,
    StringField,
    IntField,
    DateTimeField,
    ListField,
    DictField
)
from mongoengine.queryset.visitor import Q
from mongoengine.queryset import QuerySet
from bson import ObjectId
import datetime
import time
from instance.models import User, UserTopicRef, UserAction

DB_NAME = 'instance_db'

class Status(Document):
    
    meta = {
        'db_alias': 'instance_db',
        'collection': 'status'
    }

    id = ObjectIdField(primary_key=True, default=ObjectId)
    content = StringField()
    images = ListField(DictField())
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    status = IntField(default=0)
    user_id = ObjectIdField()
    like_count = IntField(default=0)
    bury_count = IntField(default=0)
    topic_id = ObjectIdField()
    location = DictField()
    visible = IntField(default=0)
    
    def pack(self, user_id=None):
        datums = {}

        u = User.objects(id=ObjectId(self.user_id)).first()
        if not u:
            u = User()
        datums['user'] = u.pack()

        datums['topic'] = {}
        t = Topic.objects(id=ObjectId(self.topic_id)).first()
        if t:
            datums['topic'] = t.pack()
        

        imgs = []
        for im in self.images:
            im['url'] = 'http://image.sleen.top/'+im['url']
           # im = 'http://image.sleen.top/'+im
            imgs.append(im)

        datums['images'] = imgs

        datums['id'] = str(self.id)
        datums['content'] = self.content
        datums['created_at'] = self.created_at.isoformat()
        datums['updated_at'] = self.updated_at.isoformat()
        datums['status'] = self.status
        datums['like_count'] = self.like_count
        datums['is_liked'] = self.is_liked(user_id)
        datums['bury_count'] = self.bury_count
        datums['location'] = self.location
        datums['visible'] = self.visible
        datums['at'] = self.at
        datums['topics'] = self.topics
        return datums


    @property
    def likers(self):
        rels = UserAction.objects(status_id=self.id, action=UserAction.ACTION_LIKE)
        return list([str(rel.user_id) for rel in rels])


    def is_liked(self, user_id):
        user_id = str(user_id)
        return user_id and user_id in self.likers

    @property
    def shielders(self):
        rels = UserAction.objects(status_id=self.id, action=UserAction.ACTION_SHIELD)
        return list([str(rel.user_id) for rel in rels])

    def is_shield(self, user_id):
        user_id = str(user_id)
        return user_id and user_id in self.shielders

    @property
    def at(self):
        at = StatusAt.objects(status_id=self.id).first()
        print(at)
        if not at:
            return []
        print(at.pack())
        return at.pack()

    @property
    def topics(self):
        rels = StatusTopicRef.objects(status_id=self.id)
        tids = [rel.topic_id for rel in rels]
        ts = Topic.objects(id__in=tids)
        print(ts)
        return [t.pack() for t in ts]


class TopicQuerySet(QuerySet):

    def get_any(self, id=None, name=None):
        return self.filter(Q(name=name)|Q(id=ObjectId(id))).first()

class Topic(Document):

    meta = {
        'db_alias': 'instance_db',
        'queryset_class': TopicQuerySet
    }

    id = ObjectIdField(primary_key=True, default=ObjectId)
    name = StringField()
    logo = StringField()
    desc = StringField()
    type = IntField()
    status = IntField(default=0)
    level = IntField(default=0)
    user_id = ObjectIdField()  # created by user 
    joined_count = IntField(default=0)
    created_at = DateTimeField(default=datetime.datetime.now)


    def save(self, *args, **kwargs):
        if not self.logo:
            self.logo = 'https://image.sleen.top/default.jpg'
        if self.joined_count < 0:
            self.joined_count = 0
        return super(Topic, self).save(*args, **kwargs)


    @property
    def joiners(self):
        rels = UserTopicRef.objects(topic_id=self.id, action=UserTopicRef.JOIN)
        return [str(rel.user_id) for rel in rels]

    def is_joined(self, user_id):
        user_id = str(user_id)
        return user_id and user_id in self.joiners

    def pack(self, user_id=None, with_user=True):
        datums = {}

        if with_user:
            u = User.objects(id=ObjectId(self.user_id)).first()
            if u:
                datums['user'] = u.pack()

        
        datums['joined'] = self.is_joined(user_id)

        datums['id'] = str(self.id)
        datums['name'] = self.name
        datums['desc'] = self.desc
        datums['logo'] = self.logo
        datums['type'] = self.type
        datums['status'] = self.status
        datums['level'] = self.level
        datums['joined_count'] = self.joined_count
        datums['created_at'] = self.created_at.isoformat()

        return datums

class StatusTopicRef(Document):
    meta = {
        'db_alias': 'instance_db'
    }

    id = ObjectIdField(primary_key=True, default=ObjectId)
    status_id = ObjectIdField()
    topic_id = ObjectIdField()
    created_at = DateTimeField(default=datetime.datetime.now)

class StatusAt(DynamicDocument):
    meta = {
        'db_alias': 'instance_db'
    }

    id = ObjectIdField(primary_key=True, default=ObjectId)
    status_id = ObjectIdField()
    users = ListField(DictField())
    created_at = DateTimeField(default=datetime.datetime.now)

    def pack(self):
        return self.users