# coding=utf-8
# author:xsl

from flask_restful import Resource
from instance.errors import MissingRequiredParameter


class Users(Resource):

    def get(self, *args, **kwargs):
        return {'name': 'Tom'}


    def post(self, *args, **kwargs):
        raise MissingRequiredParameter(['id'])


    def _follow(self):
        return {'ok': 1}
