# coding=utf-8
# author:xsl

import json
import smtplib
from functools import wraps
from email.mime.text import MIMEText
from flask import g, make_response, jsonify

from twilio.rest import Client
from qcloudsms_py import SmsSingleSender
from qcloud_cos import CosConfig, CosS3Client
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20190711 import sms_client, models

from instance import settings
from instance.errors import LoginRequiredError


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = getattr(g, 'user_id', None)
        if not user_id:
            raise LoginRequiredError()
        return func(*args, **kwargs)
    return wrapper


def output_json(data, code, headers=None, error=None, extra=None):
    
    try:
        msg = data.get('message')
    except:
        msg = None

    if msg:
        error = msg
        data = None
    
    try:
        txt = data.get('txt')
    except:
        txt = None

    if txt:
        resp = make_response(txt, code)
        return resp

    resp_data = {
        'data': data,
        'success': error is None,
        'error': error,
        'extra': extra
    }
    
    resp = make_response(jsonify(resp_data), code)
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
        print(e)
        return False
    code = int(result.get('result', -1))
    if code != 0:
        return False
    return True

def send_sms_v3(to, content):
    try:
        appid = settings.SMS_TENC_ID
        appkey = settings.SMS_TENC_KEY
        cred = credential.Credential(appid, appkey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "sms.tencentcloudapi.com"
        
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = sms_client.SmsClient(cred, "ap-beijing", clientProfile) 

        req = models.SendSmsRequest()
        p = {
            'PhoneNumberSet': to,
            'TemplateParamSet': [content],
            'TemplateID': '211830',
            'SmsSdkAppid': '1400208313'
        }
        req.from_json_string(json.dumps(p))
        resp = client.SendSms(req)
        print(resp)
        print(resp.to_json_string())
        return True

    except TencentCloudSDKException as err:
        print(err)
        return False

def send_sms_code(to, code):
    content = '验证码%s，如非本人操作请忽略。' % code
    return send_sms_v2(to, content)


def send_email(to, subject, content):
    msg = MIMEText(content.encode('utf8'), 'html', 'utf8')
    msg['From'] = settings.EMAIL_ADMIN
    msg['To'] = to
    msg['Subject'] = subject
    try:
        smtp = smtplib.SMTP_SSL(settings.EMAIL_SMTP, settings.EMAIL_SMTP_PORT)
        smtp.ehlo()
        smtp.login(settings.EMAIL_ADMIN, settings.EMAIL_ADMIN_PWD)
        smtp.sendmail(settings.EMAIL_ADMIN, to, msg.as_string())
        smtp.close()
    except Exception as e:
        print(e)
        return False
    return True

def send_email_code(to, code):
    subject = '[Instance]验证码为%s' % code
    content = '<h5>验证码:%s  (10分钟内有效)</h5>' % code
    return send_email(to, subject, content)


cos_config = CosConfig(Region='ap-beijing', 
        SecretId=settings.COS_SECRET_ID, 
        SecretKey=settings.COS_SECRET_KEY, Token=None)
cos_client = CosS3Client(cos_config)


def query_paging(qs, cursor, direction, count):
    if direction > 0 and cursor:
        kw = {'id__gt': cursor}
        qs = qs.filter(**kw).order_by('id').limit(count)
        objs = list(qs)
        objs.reverse()
    elif direction > 0 and not cursor:
        qs = qs.order_by('-id').limit(count)
        objs = list(qs)
    elif direction < 0 and cursor:
        kw = {'id__lt': cursor}
        qs = qs.filter(**kw).order_by('-id').limit(count)
        objs = list(qs)
    else:
        objs = []
    return objs

