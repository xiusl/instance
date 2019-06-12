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
from instance.models import User

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
    digg_count = IntField(default=0)
    bury_count = IntField(default=0)
    


    def pack(self, user_id=None):
        u = User.objects(id=ObjectId(self.user_id)).first()
        if not u:
            u = User()
        s_dict = {
            'id': str(self.id),
            'content': self.content,
            'images': self.images,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'status': self.status,
            'digg_count': self.digg_count,
            'bury_count': self.bury_count,
            'user': u.pack(user_id)
        }
        return s_dict

