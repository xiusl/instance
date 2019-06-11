# coding=utf-8
# author:xsl

import datetime
from bson import ObjectId
from flask import g
from flask_restful import reqparse, Resource
from instance.errors import BadRequestError, ResourceDoesNotExist, MissingRequiredParameter
from instance.utils import send_sms_code, login_required
from instance.models import User, VerifyCode

parser = reqparse.RequestParser()
parser.add_argument('phone')
parser.add_argument('code')

class UserRes(Resource):

    def get(self, id):
        if not id:
            raise MissingRequiredParameter(['id'])
        user = User.objects(id=ObjectId(id)).first()
        if not user:
            raise ResourceDoesNotExist()
        c_user = g.user
        if c_user:
            return user.pack(user_id=c_user.id)
        return user.pack()

class UsersRes(Resource):

    @login_required
    def get(self):
        print("000000000")
        print(self)
        return {'name': 'Tom'}


    def post(self):
        args = parser.parse_args()
        phone = args.get('phone')
        code = args.get('code')
        if not phone or not code:
            raise MissingRequiredParameter(['phone', 'code'])
        vc = VerifyCode.get(phone)
        if int(vc.code) != int(code):
            raise BadRequestError('VerifyCode Error')
        if vc.expired_at < datetime.datetime.now():
            raise BadRequestError('VerifyCode Expired')
        user = User.objects(phone=phone).first()
        if not user:
            user = User()
            user.phone = phone
            user.password = 'Asd110#.'
            user.save()
        return user.pack(with_token=True)




class UserFollowers(Resource):

    @login_required
    def post(self, id):
        if not id:
            raise MissingRequiredParameter(['user_id'])
        user = User.objects(id=ObjectId(id)).first()
        if not user:
            raise ResourceDoesNotExist()
        c_user = g.user
        c_user.follow(user.id)
        return user.pack(user_id=c_user.id)



class Authorizations(Resource):

    def post(self):
        args = parser.parse_args()
        phone = args.get('phone')
        code = args.get('code')
        if not phone or not code:
            raise MissingRequiredParameter(['phone', 'code'])
        vc = VerifyCode.get(phone)
        if int(vc.code) != int(code):
            raise BadRequestError('VerifyCode Error')
        if vc.expired_at < datetime.datetime.now():
            raise BadRequestError('VerifyCode Expired')
        user = User.objects(phone=phone).first()
        if not user:
            user = User()
            user.phone = phone
            user.password = 'Asd110#.'
            user.save()
        return user.pack(with_token=True)


class VerifyCodes(Resource):

    def get(self):
        args = parser.parse_args()
        phone = args.get('phone')
        if not phone:
            raise MissingRequiredParameter(['phone'])
        vc = VerifyCode.create(phone)
        ok = send_sms_code(phone, vc.code)
        if not ok:
            raise BadRequestError('Send Code Failure.')
        return {'ok': 1}

