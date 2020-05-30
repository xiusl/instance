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

class ApiLog(Document):
    
    meta = {
        'db_alias': 'log_db'
    }

    id = ObjectIdField(primary_key=True, default=ObjectId)
    user_id = ObjectIdField()
    device_type = StringField()
    ip = StringField()
    path = StringField()
    created_at = DateTimeField(default=datetime.datetime.now)
    method = StringField()
    extra = DictField()

    def pack(self):
        datum = {}

        datum['id'] = str(self.id)
        datum['user_id'] = str(self.user_id)
        datum['path'] = self.path
        datum['created_at'] = self.created_at.strftime("%Y-%m-%d %H:%M:%S") #.isoformat()
        datum['device_type'] = self.device_type
        datum['ip'] = self.ip
        datum['method'] = self.method

        return datum


