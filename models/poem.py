# coding=utf-8
# author:xsl

from mongoengine import (
    Document,
    DynamicDocument,
    ObjectIdField,
    StringField,
    IntField,
    DateTimeField
)
from bson import ObjectId
import datetime
import time


class PoemAuthor(DynamicDocument):
    meta = {
        'db_alias': 'poem_db',
        'collection': 'author_a'
    }

    id = ObjectIdField(primary_key=True, default=ObjectId)
    o_id = IntField()
    idnew = StringField()
    nameStr = StringField()
    cont = StringField()
    poems_count = IntField()



    def pack(self):
        d = {
            'id': str(self.id),
            #'o_id': self.o_id,
            #'idnew': self.idnew,
            'name': self.nameStr,
            'desc': self.cont,
            'poems_count': self.poems_count
        }
        return d


class Poem(DynamicDocument):
    meta = {
        'db_alias': 'poem_db',
        'collection': 'poem_a'
    }

    id = ObjectIdField(primary_key=True, default=ObjectId)
    nameStr = StringField()
    author = StringField()
    chaodai = StringField()
    cont = StringField()
    o_id = IntField()
    tag = StringField()

    def pack(self):
        tags = self.tag.split('|')
        d = {
            'id': str(self.id),
            'name': self.nameStr,
            'author': self.author,
            'dynasty': self.chaodai,
            'content': self.cont,
            'tags': tags
        }
        return d
