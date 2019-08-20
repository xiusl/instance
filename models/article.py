# coding=utf-8
# author:xsl

from mongoengine import (
    Document,
    ObjectIdField,
    StringField,
    IntField,
    ListField,
    DateTimeField
)
from bson import ObjectId
import datetime
import time

DB_NAME = 'instance_db'

class Article(Document):
    meta = {
        'db_alias': DB_NAME        
    }

    id = ObjectIdField(primary_key=True, default=ObjectId)
    title = StringField()
    original_url = StringField(unique=True)
    original_id = StringField()
    content = StringField()
    author = StringField()
    created_at = DateTimeField(default=datetime.datetime.now)
    source = StringField()
    images = ListField()
    type = StringField()
    status = IntField(default=0)

    def pack(self):
        art_dict = {
            'id': str(self.id),
            'title': self.title,
            'content': self.content,
            'original_url': self.original_url,
            'orginal_id': self.orginal_id,
            'author': self.author,
            'created_at': self.created_at,
            'source': self.source,
            'type': self.type,
            'status': self.status,
            'images': self.images
        }
        return art_dict
