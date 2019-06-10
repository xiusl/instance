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

DB_NAME = 'instance_db'

class Status(Document):
    
    meta = {
        'db_alias': DB_NAME
    }

    id = ObjectIdField(primary_key=True, default=ObjectId)
    content = StringField()
    images = ListField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    status = IntField()
    user_id = ObjectIdField()
    digg_count = IntField()
    bury_count = IntField()
    

