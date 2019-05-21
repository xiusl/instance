# coding=utf-8
# author:xsl

from flask import make_response
import json
from instance import settings
from twilio.rest import Client

from qcloudsms_py import SmsSingleSender

def output_json(data, code, headers=None, error=None, extra=None):
    msg = data.get('message')
    if msg:
        error = msg
        data = None

    resp_data = {
        'data': data,
        'success': error is None,
        'error': error,
        'extra': extra
    }
    
    resp = make_response(json.dumps(resp_data), code)
    resp.headers.extend(headers or {})
    return resp


def send_sms(to, content):
    account_sid = settings.SMS_ACCOUNT
    auth_token = settings.SMS_TOKEN
    client = Client(account_sid, auth_token)
    message = client.messages.create(
            body=content,
            from_='+12063396365',
            to=to)
    if message.error_code:
        return False
    return True

def send_sms_v2(to, content):
    appid = settings.SMS_TENC_ID
    appkey = settings.SMS_TENC_KEY
    ssender = SmsSingleSender(appid, appkey)
    sms_type = 0
    try:
        result = ssender.send(sms_type,
                86, 
                to, 
                content,
                extend='',
                ext='')
    except Exception as e:
        return False
    code = int(result.get('result'))
    if code != 0:
        return False
    return True

def send_sms_code(to, code):
    content = '验证码%s，如非本人操作请忽略。' % code
    return send_sms_v2(to, content)
