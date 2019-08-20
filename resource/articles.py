# coding=utf-8
# author:xsl

from flask import g
from flask_restful import reqparse, Resource
from instance.models import Article
from instance.errors import BadRequestError, ResourceDoesNotExist

parser = reqparse.RequestParser()
_args = ['url']
for _arg in _args:
    parser.add_argument(_arg)

class ArticleRes(Resource):

    def post(self):
        args = parser.parse_args()
        url = args.get('url')
         
        return {'ok':1}


    def get(self):
        args = parser.parse_args()
        url = args.get('url')
        art = Article.objects(original_url=url).first()
        if not art:
            raise ResourceDoesNotExist()

        return art.pack()
