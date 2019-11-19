# coding=utf-8
# author:xsl

from flask import Flask, g, current_app, request, make_response
from flask_restful import Api
from flask_cors import CORS

import settings
from instance.models import User
from instance.utils import output_json, cos_client
from instance.resource import (
    StatusesRes, 
    StatusRes, 
    Authorizations, 
    UsersRes, 
    UserRes,
    VerifyCodes, 
    UserFollowers,
    UserFolloweds,
    UserStatusesRes,
    StatusLikesRes,
    UserStatusLikesRes,
    UserPasswordRes,
    ArticleSpiderRes,
    ArticlesRes,
    ArticleRes,
    SourcesRes,
    SettingsRes,
    SettingWxRes,
    SettingPingRes,
    SpiderArtsRes,
    PoemAuthorsRes,
    PoemsRes,
    PoemTagsRes,
)
from instance.errors import ApiBaseError, ResourceDoesNotExist, MissingRequiredParameter

class MyApi(Api):

    def __init__(self, *args, **kwargs):
        super(MyApi, self).__init__(*args, **kwargs)
        self.representations = {
            'application/json': output_json,
        }

        
    def handle_error(self, e):
        for val in current_app.error_handler_spec.values():
            for handler in val.values():
                registered_error_handlers = list(filter(lambda x: isinstance(e, x), handler.keys()))
                if len(registered_error_handlers) > 0:
                    raise e
        return super().handle_error(e)

errors = {
    'NotFound': {
        'message': 'Endpoint notFound',
        'status': 404,
    }
}
    

app = Flask(__name__)
api = MyApi(app, catch_all_404s=True, errors=errors)
CORS(app, supports_credentials=True)

@app.before_request
def before_request():
    token = request.headers.get("X-Token")
    g.user = User()
    g.user_id = None
    if token:
        u = User.get_by_token(token)
        g.user = u
        g.user_id = u.id if u else None

    source = request.headers.get("X-Type") or ""
    g.source = source 

@app.errorhandler(ApiBaseError)
def handle_api_error(error):
    return output_json(error.to_dict(), error.code)

api.add_resource(Authorizations, '/authorizations')
api.add_resource(UsersRes, '/users')
api.add_resource(UserRes, '/users/<id>')
api.add_resource(UserPasswordRes, '/users/<id>/password')
api.add_resource(VerifyCodes, '/verifycodes')
api.add_resource(UserFollowers, '/users/<id>/followers')
api.add_resource(UserFolloweds, '/users/<id>/followeds')
api.add_resource(StatusesRes, '/statuses')
api.add_resource(StatusRes, '/statuses/<id>')
api.add_resource(UserStatusesRes, '/users/<user_id>/statuses')
api.add_resource(StatusLikesRes, '/statuses/<id>/likes')
api.add_resource(UserStatusLikesRes, '/users/<id>/likes/statuses')
api.add_resource(ArticleSpiderRes, '/articles/spider')
api.add_resource(ArticlesRes, '/articles')
api.add_resource(ArticleRes, '/articles/<id>')
api.add_resource(SourcesRes, '/sources')
api.add_resource(SettingsRes, '/settings')
api.add_resource(SettingWxRes, '/setting/wx')
api.add_resource(SettingPingRes, '/setting/ping')
api.add_resource(SpiderArtsRes, '/spiderarts')


api.add_resource(PoemAuthorsRes, '/p/authors')
api.add_resource(PoemsRes, '/p/poems')
api.add_resource(PoemTagsRes, '/p/tags')

if __name__ == '__main__':
    app.run(debug=True)




