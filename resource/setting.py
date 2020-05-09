# coding=utf-8
# author:xsl

import hashlib
import requests
from flask import request
from flask_restful import reqparse, Resource
from instance.utils import cos_client, login_required
from qiniu import Auth
import settings

parser = reqparse.RequestParser()
_args = ['mime_type', 'code']
for _arg in _args:
    parser.add_argument(_arg)

class SettingsRes(Resource):
    
    @login_required
    def get(self):
        args = parser.parse_args()
        mime_type = args.get('mime_type') or 'image/*'
        resp = cos_client.get_auth(
            Method = 'POST',
            Bucket = 'shilin-1255431184',
            Headers = {
                'Content-Type': mime_type    
            },
            Key = '/',
            Expired = 3600
        )
        return resp

class SettingPingRes(Resource):

    @login_required
    def get(self):
        return {'ok': 1}


class QiniuTokenRes(Resource):

    @login_required
    def get(self):
        access_key = settings.QINIU_ACCESS
        secret_key = settings.QINIU_SECRET
        q = Auth(access_key, secret_key)
        bucket_name = 'mizou'
        policy = {
            'returnBody': '{"key": $(key), "hash": $(etag), "w": $(imageInfo.width), "h": $(imageInfo.height)}'
        }
        token = q.upload_token(bucket_name, None, 3600, policy)
        return token

_args2 = ['signature', 'timestamp', 'msg_signature', 'nonce', 'echostr']
for _arg2 in _args2:
    parser.add_argument(_arg2)

try:
  import xml.etree.cElementTree as ET
except ImportError:
  import xml.etree.ElementTree as ET

from instance.wxsdk import WXBizMsgCrypt, WXBizDataCrypt
  
class SettingWxRes(Resource):

    def get(self):
        args = parser.parse_args()
        signature = args.get('signature') or ''
        timestamp = args.get('timestamp') or ''
        nonce = args.get('nonce') or ''
        echostr = args.get('echostr') or ''
        token = 'fkasn123dkda123nlkinjkd12j3'
        sortlist = [timestamp, nonce, token]
        sortlist.sort()
        sha = hashlib.sha1()
        sha.update("".join(sortlist).encode('utf8'))
        sign = sha.hexdigest()
        if sign == signature:
            return {'txt':echostr}
        return {'txt':'error'}


    def post(self):
        args = parser.parse_args()
        nonce = args.get('nonce') or ''
        msg_sign = args.get('msg_signature') or ''
        timestamp = args.get('timestamp') or ''

        data = request.get_data().decode('utf8')
        aesKey = settings.WX_AES_KEY 
        appid = 'wx40ed1fc0ef59c172'
        token = settings.WX_TOKEN 
        decrypt_test = WXBizMsgCrypt(token, aesKey, appid)
        re, d = decrypt_test.DecryptMsg(data, msg_sign, timestamp, nonce)
        root = ET.fromstring(d)
        msg = root.find('Content').text

        if msg.startswith('http'):
            url = 'http://192.144.171.238/spider'
            data = {'url': msg}
        headers = {'Content-Type':'application/json'}
        res = requests.post(url, json=data, headers=headers, verify=False)

        return {'txt':'success'}

class SettingWxMiniRes(Resource):

    def post(self):
        args = parser.parse_args()
        code = args.get('code')
        if code:
            appid = settings.WX_MINI_ID
            secret = settings.WX_MINI_SECRET
            url = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'.format(appid, secret, code)
            resp = requests.get(url)
            data = resp.json()
            print(data)
            return {'txt': '123'}


        enc_data = args.get('enc_data')

        appId = ''
        sessionKey = ''
        iv = args.get('iv')

        pc = WXBizDataCrypt(appId, sessionKey)
        
        print(pc.decrypt(encryptedData, iv))
        return {'txt': '12'}

