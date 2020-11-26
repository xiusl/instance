# coding=utf-8
# author:xsl

import requests
import json
from flask import g, current_app
from flask_restful import reqparse, Resource
from bson import ObjectId
from instance.models import Product, ProVersion
from instance.utils import login_required, query_paging


parser = reqparse.RequestParser()
_args = ['id', 'name', 'icon', 'app_url', 'manifest_url', 'desc']
for _arg in _args:
    parser.add_argument(_arg)


class ProductsRes(Resource):

    def get(self):
        args = parser.parse_args()
        products = Product.objects()
        return {'products': [p.pack() for p in products]}


    def post(self):
        args = parser.parse_args()


