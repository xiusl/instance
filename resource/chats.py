# coding=utf-8
# author:xsl

import datetime
from bson import ObjectId
from flask import g
from flask_restful import reqparse, Resource
from instance.errors import *
from instacne.utils import login_required
from instacne.models import User, Chatroom

parser = reqparse.RequestParser()
_args = ['name']
for _arg in _args:
    parser.add_argument(_arg)

class ChatroomsRes(Resource):

    @login_required
    def post(self, id):
        return ""
