# coding=utf-8
# author:xsl

from mongoengine import (
    Document,
    ObjectIdField,
    StringField,
    IntField,
    DateTimeField
)
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
import datetime
import time
import hmac, hashlib, base64
import random

DB_NAME = 'instance_db'


def hmac_sha256(key, message):
    key = key.encode('utf8')
    message = message.encode('utf8')
    sign = hmac.new(key, message, digestmod=hashlib.sha256).digest()
    sign = '.'.join([('%02x' % b) for b in sign])
    return sign


class User(Document):
    pk_name = 'id'

    meta = {
        'db_alias': DB_NAME
    }

    id = ObjectIdField(primary_key=True, default=ObjectId)
    phone = StringField(unique=True)
    email = StringField()
    name = StringField()
    password = StringField()
    avatar = StringField()
    desc = StringField()
    level = IntField(default=0)
    type = IntField(default=0)
    created_at = DateTimeField(default=datetime.datetime.now)
    status = IntField(default=0)
    followed_count = IntField(default=0)
    following_count = IntField(default=0)

    def save(self, *args, **kwargs):
        if self.password and \
                (self.password.count('$') < 2 or len(self.password) < 50):
            self.password = generate_password_hash(self.password)
        if not self.avatar:
            self.avatar = 'https://image.sleen.top/default.jpg'
        if not self.name and self.email:
            self.name = self.email.split("@")[0]
        if not self.name and self.phone:
            self.name = 'user%s' % self.phone[-4:]
        return super(User, self).save(*args, **kwargs)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_token(self, timestamp=None, expired_at=None):
        timestamp = timestamp or int(time.time())
        expired_at = expired_at or (timestamp+86400*30)
        message = '%s:%s:%s' % (self.id, timestamp, expired_at)
        sign = hmac_sha256(self.password, message)
        signed_message = '%s$%s' % (message, sign)
        token = base64.b64encode(signed_message.encode('utf8'))
        return token.decode('utf8')

    @property
    def is_admin(self):
        return self.level == 9

    @property
    def followers(self):
        rels = UserRelation.objects(followed_id=self.id)
        return list([rel.follower_id for rel in rels])

    @property
    def followeds(self):
        # self follow
        rels = UserRelation.objects(follower_id=self.id)
        return list([rel.followed_id for rel in rels])

    def is_following(self, user_id):
        u_id= ObjectId(user_id)
        return u_id and u_id in self.followeds

    def is_followed(self, user_id):
        u_id = ObjectId(user_id)
        print(u_id)
        return u_id and u_id in self.followers

    def follow(self, user_id):
        if user_id in self.followeds:
            return False
        rel = UserRelation(followed_id=user_id, follower_id=self.id)
        rel.save()
        return True

    def unfollow(self, user_id):
        if user_id in self.followers:
            return False
        rel = UserRelation.objects(followed_id=user_id, follower_id=self.id)
        if not rel:
            return False
        rel.delete()
        return True

    @classmethod
    def get_by_token(cls, token):
        try:
            token = base64.b64decode(token).decode('utf8')
            message, sign = token.split('$')
            user_id, ts, expired_at = message.split(':')
        except:
            return None
        if int(time.time()) > int(expired_at):
            return None

        user = cls.objects(id=user_id).first()
        if not user:
            return None

        if sign != hmac_sha256(user.password, message):
            return None

        return user


    def pack(self, user_id=None, with_token=False):
        user_dict = {
            'id': str(self.id),
            'name': self.name,
            'desc': self.desc,
            'phone': self.phone,
            'email': self.email,
            'avatar': self.avatar,
            'created_at': self.created_at,
            'status': self.status,
            'level': self.level,
            'type': self.type,
            'is_followed': self.is_following(user_id),
            'is_following': self.is_followed(user_id),
            'following_count': self.following_count,
            'followed_count': self.followed_count
        }
        if with_token:
            user_dict['token'] = self.get_token()
        return user_dict


class UserRelation(Document):
    meta = {
        'db_alias': DB_NAME        
    }

    id = ObjectIdField(primary_key=True, default=ObjectId)
    follower_id = ObjectIdField()
    followed_id = ObjectIdField()
    created_at = DateTimeField(default=datetime.datetime.now())



class VerifyCode(Document):
    meta = {
        'db_alias': DB_NAME,
        'index_background': True,
        'indexes': [
            'key',
            {'fields': ('expired_at', ), 'expireAfterSeconds': 0},
        ],
    }

    id = ObjectIdField(primary_key=True, default=ObjectId)
    key = StringField()
    code = StringField()
    expired_at = DateTimeField()
    created_at = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def get(cls, key):
        return cls.objects(key=key).order_by("-id").first()

    @classmethod
    def create(cls, key, ttl=36000):
        vc = cls(key=key)
        vc.code = str(random.randint(1000, 9999))
        vc.expired_at = datetime.datetime.now() + \
                datetime.timedelta(seconds=ttl)
        vc.save()
        return vc


class UserAction(Document):
    meta = {
        'db_alias': DB_NAME
    }
    
    ACTION_LIKE = 'like'
    ACTION_UNLIKE = 'unlike'


    id = ObjectIdField(primary_key=True, default=ObjectId)
    status_id = ObjectIdField()
    user_id = ObjectIdField()
    action = StringField()
    created_at = DateTimeField(default=datetime.datetime.now)



