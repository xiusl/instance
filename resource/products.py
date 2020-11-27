# coding=utf-8
# author:xsl

import requests
import json
from flask import g, current_app
from flask_restful import reqparse, Resource
from bson import ObjectId
from instance.models import Product, ProVersion
from instance.utils import login_required, query_paging
from instance.errors import (
    BadRequestError,
    ResourceDoesNotExist,
    MissingRequiredParameter
)

parser = reqparse.RequestParser()
_args = ['id', 'name', 'icon', 'code', 'build', 'app_url', 'manifest_url', 'desc']
for _arg in _args:
    parser.add_argument(_arg)


class ProductsRes(Resource):

    def get(self):
        args = parser.parse_args()
        products = Product.objects()
        return {'products': [p.pack() for p in products]}


    def post(self):
        args = parser.parse_args()
        name = args.get('name')
        if not name:
            raise MissingRequiredParameter(['name'])

        desc = args.get('desc') or ''
        icon = args.get('icon') or ''
        appstore_url = args.get('appstore_url') or ''
        p = Product(name=name,desc=desc,icon=icon,appstore_url=appstore_url)
        p.save()
        return p.pack()


class ProductRes(Resource):

    def get(self, id):
        p = Product.objects(id=ObjectId(id)).first()
        if not p:
            raise ResourceDoesNotExist
        return p.pack()


class ProductVersionsRes(Resource):

    def get(self, id):
        vs = ProVersion.objects(product_id=ObjectId(id))
        return [v.pack() for v in vs]

    def post(self, id):
        p = Product.objects(id=ObjectId(id)).first()
        if not p:
            raise ResourceDoesNotExist
        args = parser.parse_args()
        name = args.get('name')
        if not name:
            raise MissingRequiredParameter(['name'])
        code = args.get('code')
        if not code:
            raise MissingRequiredParameter(['code'])
        build = args.get('build_code')
        app_url = args.get('app_url')
        if not app_url:
            raise MissingRequiredParameter(['app_url'])
        type = args.get('type')
        m_url = args.get('manifest_url')
        
        pv = ProVersion(name=name,code=code,app_url=app_url)
        pv.build_code = build
        pv.type = type
        pv.manifest_url = m_url
        pv.product_id = p.id
        pv.save()
        return pv.pack()

class VersionRes(Resource):

    def get(self, id):
        v = ProVersion.objects(id=ObjectId(id)).first()
        if not v:
            raise ResourceDoesNotExist
        return v.pack()
