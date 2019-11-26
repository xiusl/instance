# coding=utf-8
# author:xsl

from mongoengine import (
    Document,
    ObjectIdField,
    StringField,
    IntField,
    DateTimeField,
    ListField,
    DictField
)
from bson import ObjectId
import datetime
import time
from instance.models import User, UserAction

DB_NAME = 'instance_db'

class Status(Document):
    
    meta = {
        'db_alias': DB_NAME
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
    


    def pack(self, user_id=None):
        u = User.objects(id=ObjectId(self.user_id)).first()
        if not u:
            u = User()

        imgs = []
        for im in self.images:
            im['url'] = 'http://image.sleen.top'+im['url']
            imgs.append(im)

        s_dict = {
            'id': str(self.id),
            'content': self.content,
            'images': imgs,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'status': self.status,
            'like_count': self.like_count,
            'is_liked': self.is_liked(user_id),
            'bury_count': self.bury_count,
            'user': u.pack(user_id)
        }
        return s_dict


    @property
    def likers(self):
        rels = UserAction.objects(status_id=self.id, action=UserAction.ACTION_LIKE)
        return list([str(rel.user_id) for rel in rels])


    def is_liked(self, user_id):
        user_id = str(user_id)
        return user_id and user_id in self.likers



