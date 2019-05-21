# coding=utf-8
# author:xsl

from flask_restful import reqparse, Resource
from instance.errors import BadRequestError, MissingRequiredParameter
from instance.utils import send_sms_code
from instance.models import VerifyCode

parser = reqparse.RequestParser()
parser.add_argument('phone')

class Users(Resource):

    def get(self, *args, **kwargs):
        return {'name': 'Tom'}


    def post(self):
        args = parser.parse_args()
        raise MissingRequiredParameter(['id'])


    def _follow(self):
        return {'ok': 1}


class UserFollowers(Resource):

    def post(self, user_id):
        return {'ok': 1}



class VerifyCodes(Resource):

    def get(self):
        args = parser.parse_args()
        phone = args.get('phone')
        vc = VerifyCode.create(phone)
        ok = send_sms_code(phone, vc.code)
        if not ok:
            raise BadRequestError('Send Code Failure.')
        return {'ok': 1}

