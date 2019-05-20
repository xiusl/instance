# coding=utf-8
# author:xsl

from flask_restful import Resource

class Users(Resource):

    def get(self, *args, **kwargs):
        return {'name': 'Tom'}


