# coding=utf-8
# author:xsl

from hashlib import sha1
import time
import requests

from instance import settings

def registIMUser(user_id, name=None, avatar=None):
    url = "https://api.netease.im/nimserver/user/create.action"
    headers = createIMHeader()
    data = dict()
    data['accid'] = user_id
    if name:
        data['name'] = name
    if avatar:
        data['icon'] = avatar
    resp = requests.post(url, headers=headers, data=data)

    data = resp.json()
    print(data)
    code = data.get('code')
    if code == 200:
        return True, data.get('info').get('token')
    return False, data.get('desc')


def refreshIMToken(user_id):
    url = "https://api.netease.im/nimserver/user/refreshToken.action"

    headers = createIMHeader()
    data = {"accid": user_id}
    resp = requests.post(url, headers=headers, data=data)
    data = resp.json()
    code = data.get('code')
    print('刷新im令牌', resp)
    if code == 200:
        return True, data.get('info').get('token')
    return False, data.get('desc')


def updateIMUserInfo(user_id, name=None, avatar=None):
    url = "https://api.netease.im/nimserver/user/updateUinfo.action"
    headers = createIMHeader()
    data = dict()
    data["accid"] = user_id
    if name:
        data["name"] = name
    if avatar:
        if not avatar.startswith('http'):
            data['icon'] = 'https://image.sleen.top/' + avatar
        else:
            data['icon'] = avatar
    print(data)
    resp = requests.post(url, headers=headers, data=data)
    data = resp.json()
    code = data.get('code')
    if code == 200:
        print("update im user info ok")
        return True
    print("update im user info error")
    return True

def createIMHeader():
    app_key = settings.IM163_APP_KEY
    app_secret = settings.IM163_APP_SECRET
    nonce = "likeorgim"
    curtime = int(time.time())
    headers = {
        "AppKey": app_key,
        "Nonce": nonce,
        "CurTime": str(curtime),
        "CheckSum": checkSum(app_secret, nonce, curtime),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return headers

def checkSum(secret, nonce, cur_time):

    message = '%s%s%s' % (secret, nonce, cur_time)
    s1 = sha1()
    s1.update(message.encode('utf8'))
    msg_s1 = s1.hexdigest()
    return msg_s1
