# coding=utf-8
# author:xsl

import datetime
import time
from mongoengine import (
    Document,
    ObjectIdField,
    StringField,
    IntField,
    DateTimeField
)
from bson import ObjectId

DB_NAME = 'instance_db'


class ChatRoom(Documnet):
    pk_name = 'id'

    meta = {
        'db_alias': DB_NAME
    }

    id = ObjectIdField(primary_key=True, default=ObjectId)
    name = StringField()
    user_id = ObjectField()
    announcement = StringField()
    broadcasturl = StringField()
    extra = StringField()
    queuelevel = IntField()
    valid = IntField()
    room_id = StringField()
    voice_id = StringField()
    type = IntField() # 1 文字 2 语音
    online_num = IntField()

