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


class Product(DynamicDocument):
    meta = {
        'db_alias': 'potato_db'
    }
    
    id = ObjectIdField(primary_key=True, default=ObjectId)
    name = StringField()
    desc = StringField()
    icon = StringField()
    appstore_url = StringField()
    status = IntField(default=0)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    def pack(self):
        datums = {}
        datums['id'] = str(self.id)
        datums['name'] = self.name
        datums['desc'] = self.desc
        datums['icon'] = self.icon
        datums['appstore_url'] = self.appstore_url

        return datums

class ProVersion(DynamicDocument):
    meta = {
        'db_alias': 'potato_db'
    }

    id = ObjectIdField(primary_key=True, default=ObjectId)
    name = StringField()
    desc = StringField()
    code = StringField()
    build_code = StringField()
    app_url = StringField()
    type = StringField()
    product_id = ObjectIdField()
    manifest_url = StringField()
    created_at = DateTimeField(default=datetime.datetime.utcnow)


    def pack(self):
        datums = {}
        datums['id'] = str(self.id)
        datums['name'] = self.name
        datums['desc'] = self.desc
        datums['code'] = self.code
        datums['build_code'] = self.build_code
        datums['app_url'] = self.app_url
        datums['manifest_url'] = self.manifest_url
        datums['created_at'] = self.created_at.isoformat()
        datums['ios_down_url'] = 'itms-services://?action=download-manifest&url=' + str(self.manifest_url)
        
        return datums

