# coding=utf-8
# author:xsl

import os
import sys

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(PROJECT_DIR, os.pardir)

sys.path.append(PARENT_DIR)
sys.path.append(PROJECT_DIR)

MONGO_DB = os.getenv('MONGO_DB') or 'instance_db'
MONGO_URL = os.getenv('MONGO_URL') or 'mongodb://127.0.0.1:27017/instance_db'

from mongoengine import connect
connect(alias=MONGO_DB, host=MONGO_URL,connect=False)

connect(alias='sp_db', host='mongodb://127.0.0.1:27017/sp_db',connect=False)
connect(alias='poem_db', host='mongodb://127.0.0.1:27017/poem_db',connect=False)
connect(alias='log_db', host='mongodb://127.0.0.1:27017/log_db',connect=False)
connect(alias='potato_db', host='mongodb://127.0.0.1:27017/potato_db',connect=False)

SMS_ACCOUNT = os.getenv('SMS_ACCOUNT') or ''
SMS_TOKEN = os.getenv('SMS_TOKEN') or ''


SMS_TENC_ID = os.getenv('SMS_TENC_ID') or ''
SMS_TENC_KEY = os.getenv('SMS_TENC_KEY') or ''


COS_SECRET_ID = os.getenv("COS_SECRET_ID") or "123"
COS_SECRET_KEY = os.getenv("COS_SECRET_KEY") or "456"

EMAIL_SMTP = 'smtp.exmail.qq.com'
EMAIL_SMTP_PORT = '465'
EMAIL_ADMIN = 'help@xiusl.com'
EMAIL_ADMIN_PWD = 'He110120.'

WX_AES_KEY = os.getenv('WX_AES_KEY') or ''
WX_TOKEN = os.getenv('WX_TOKEN') or ''

WX_MINI_ID = os.getenv('WX_MINI_ID') or ''
WX_MINI_SECRET = os.getenv('WX_MINI_SECRET') or ''

QINIU_ACCESS = os.getenv('QINIU_ACCESS')
QINIU_SECRET = os.getenv('QINIU_SECRET')

