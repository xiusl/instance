# coding=utf-8
# author:xsl

import time
import datetime

from mongoengine import (
    Document,
    DynamicDocument,
    ObjectIdField,
    StringField,
    IntField,
    DateTimeField
)
from bson import ObjectId

from .user import User
from .status import Status
from .article import Article


class Feedback(DynamicDocument):
    meta = {
        'db_alias': 'instance_db'
    }

    STATUS_NEED_REPLAY = 2
    STATUS_FINISHED = 1

    id = ObjectIdField(primary_key=True, default=ObjectId)
    user_id = ObjectIdField()
    content = StringField()
    contact = StringField()
    status = IntField(default=STATUS_NEED_REPLAY)
    replay = StringField()
    replay_time = DateTimeField()
    created_at = DateTimeField(default=datetime.datetime.now)
    ref_id = ObjectIdField()
    type = StringField()

    def pack(self):
        datum = {}
        datum['id'] = str(self.id)
        datum['content'] = self.content
        datum['contact'] = self.contact
        datum['status'] = self.status
        datum['replay'] = self.replay
        datum['created_at'] = self.created_at.isoformat()
        datum['type'] = self.type

        if self.replay_time:
            datum['replay_time'] = self.replay_time.isoformat()

        if self.user_id:
            u = User.objects(id=ObjectId(self.user_id)).first()
            if u:
                datum['user'] = u.pack()

        if self.ref_id:
            if self.type == 'status':
                s = Status.objects.with_id(self.ref_id)
                if s:
                    datum['obj'] = s.pack()
            elif self.type == 'article':
                a = Article.objects.with_id(self.ref_id)
                if a:
                    datum['obj'] = a.pack()

        return datum

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
        tags = []
        if len(self.tag):
            tags = self.tag.split('|')
        cols = []
        if len(self.collection):
            cols = self.collection.split('|')
        d = {
            'id': str(self.id),
            'name': self.nameStr,
            'author': self.author,
            'dynasty': self.chaodai,
            'content': self.cont,
            'tags': tags,
            'cols': cols
        }
        return d

class PoemTag(DynamicDocument):
    meta = {
        'db_alias': 'poem_db',
        'collection': 'tag_a'
    }

    id = ObjectIdField(primary_key=True, default=ObjectId)
    name = StringField()

    def pack(self):
        return {'id':str(self.id), 'name': self.name}
