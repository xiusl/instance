# coding=utf-8
# author:xsl

import hashlib
import requests
from flask import request
from flask_restful import reqparse, Resource
from instance.utils import admin_required, cos_client, login_required
from instance.models import ApiLog
import settings

parser = reqparse.RequestParser()
_args = ['page', 'count']
for _arg in _args:
    parser.add_argument(_arg)

class ApiLogRes(Resource):

    @admin_required
    def get(self):
        args = parser.parse_args()
        page = int(args.get('page') or 1)
        count = int(args.get('count') or 10)
        qs = ApiLog.objects().order_by('-created_at')
        data = qs.skip(page*count-count).limit(count)
        return {"count":qs.count(), "logs":[q.pack() for q in data]}

