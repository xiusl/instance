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
    original_url = StringField()
    original_id = StringField()
    content = StringField()
    author = StringField()
    author_idf = StringField()
    published_at = StringField()
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
            'original_id': self.original_id,
            'author': self.author,
            'published_at': self.published_at,
            'created_at': self.created_at,
            'source': self.source,
            'type': self.type,
            'status': self.status,
            'author_idf': self.author_idf,
            'images': self.images
        }
        return art_dict
