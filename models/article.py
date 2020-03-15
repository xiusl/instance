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
from instance.models import User

DB_NAME = 'instance_db'
img_crop = '?imageMogr2/thumbnail/600x/interlace/0%7CimageMogr2/gravity/center/crop/800x600'

class Article(Document):
    meta = {
        'db_alias': DB_NAME        
    }

    id = ObjectIdField(primary_key=True, default=ObjectId)
    title = StringField()
    original_url = StringField()
    original_id = StringField()
    content = StringField()
    transcoding = StringField()
    author = StringField()
    author_idf = StringField()
    published_at = DateTimeField(default=datetime.datetime.now)
    created_at = DateTimeField(default=datetime.datetime.now)
    source = StringField()
    images = ListField()
    type = StringField()
    status = IntField(default=0)
    spider = IntField(default=0)
    user_id = ObjectIdField()


    def save(self, *args, **kwargs):
        if not self.user_id:
            user = User.objects(phone='17600101706').first()
            self.user = user.id
        return super(Article, self).save(*args, **kwargs)

    def pack(self, trans=False, g_user=None):
        u = User.objects(id=ObjectId(self.user_id)).first()
        if not u:
            u = User()
        data = {}
        data['id'] = str(self.id)
        data['title'] = self.title
        if trans:
            data['content'] = self.content
            data['transcoding'] = self.transcoding
        data['original_url'] = self.original_url
        data['original_id'] = self.original_id
        data['author'] = self.author
        data['published_at'] = self.published_at.isoformat()
        data['created_at'] = self.created_at.isoformat()
        data['source'] = self.source
        data['type'] = self.type
        data['status'] = self.status
        data['author_idf'] = self.author_idf
        # data['images'] = self.images
        data['url'] = 'https://ins.sleen.top/articles/{}'.format(str(self.id))
        data['is_spider'] = self.spider
        data['user'] = u.pack(user_id=g_user)
        
        data['images'] = list([im + img_crop for im in self.images])

        return data 


class Source(Document):
    meta = {
        'db_alias': DB_NAME
    }

    id = ObjectIdField(primary_key=True, default=ObjectId)
    name = StringField()
    identifier = StringField()
    avatar = StringField()
    type = StringField()
    level = IntField(default=0)
    status = IntField(default=0)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    spider_url = StringField()
    url = StringField()


    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = 'https://images.sleen.top/default.jpg'
        return super(Source, self).save(*args,**kwargs)

    def pack(self):
        sour_dict = {
            'id': str(self.id),
            'name': self.name,
            'identifier': self.identifier,
            'avatar': self.avatar,
            'type': self.type,
            'level': self.level,
            'status': self.status,
            'url': self.url,
            'spider_url': self.spider_url,
            'created_at': self.created_at
        }
        return sour_dict

class SpArtSmp(Document):
    # 批量抓取临时存储 url
    meta = {
        'db_alias': 'sp_db',
        'collection': 'tmp'
    }

    id = ObjectIdField(primary_key=True, default=ObjectId)
    title = StringField()
    url = StringField()
    a_id = StringField()
    user_id = StringField()
    user_name = StringField()


    def pack(self):
        d = {
            'id': str(self.id),
            'a_id': self.a_id,
            'title': self.title,
            'url': self.url,
            'user_id': self.user_id,
            'user_name': self.user_name
        }
        return d

