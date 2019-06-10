# coding=utf-8
# author:xsl

import datetime
from flask_restful import reqparse, Resource
from instance.errors import BadRequestError, MissingRequiredParameter
from instance.utils import send_sms_code, login_required
from instance.models import User, VerifyCode

parser = reqparse.RequestParser()
parser.add_argument('phone')
parser.add_argument('code')

class Users(Resource):

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


    def _follow(self):
        return {'ok': 1}


class UserFollowers(Resource):

    def post(self, user_id):
        return {'ok': 1}


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

