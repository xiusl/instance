# coding=utf-8
# author:xsl

import os

MONGO_DB = os.getenv('MONGO_DB') or 'instance_db'
MONGO_URL = os.getenv('MONDO_URL') or 'mongodb://127.0.0.1:27017/instance_db'


from mongoengine import connect
connect(alias=MONGO_DB, host=MONGO_URL)



SMS_ACCOUNT = os.getenv('SMS_ACCOUNT') or ''
SMS_TOKEN = os.getenv('SMS_TOKEN') or ''


SMS_TENC_ID = os.getenv('SMS_TENC_ID') or ''
SMS_TENC_KEY = os.getenv('SMS_TENC_KEY') or ''

