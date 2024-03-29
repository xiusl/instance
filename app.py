# coding=utf-8
# author:xsl

import logging
from bson import ObjectId
from flask import Flask, g, current_app, request, make_response
from flask_restful import Api
from flask_cors import CORS

import settings
from instance.models import User, ApiLog
from instance.utils import output_json, cos_client
from instance.maps import (
    map_user, 
    map_status, 
    map_article, 
    map_poem,
    map_other,
)
from instance.errors import (
    ApiBaseError, 
    ResourceDoesNotExist, 
    MissingRequiredParameter,
)

class MyApi(Api):

    def __init__(self, *args, **kwargs):
        super(MyApi, self).__init__(*args, **kwargs)
        self.representations = {
            'application/json': output_json,
        }
        self.debug = self.app.config['DEBUG']
        
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
        g.user_type = u.type if u else 0

    source = request.headers.get("X-Type") or "web"
    g.source = source 


@app.teardown_request
def teardown_request(e):
    ip = request.headers.get('X-Real-IP') or ''
    user_id = g.user_id
    path = request.path
    method = request.method
    app.logger.info('User {} at {} request {}'.format(user_id, ip, path))
    if 'favicon.ico' in path:
        return 
    
    source = getattr(g, 'source', 'web')
    if source == 'web':
        return 
    l = ApiLog()
    if user_id:
        l.user_id = ObjectId(user_id)
    l.ip = ip
    l.device_type = g.source or ''
    l.path = path
    l.method = method
    l.save()


@app.errorhandler(Exception)
def handle_app_error(error):
    if app.config['DEBUG']:
        raise error
    if error.code == 404:
        return output_json('', error.code, error="endpoint not found")
    return output_json('', 500, error=str(error))

@app.errorhandler(ApiBaseError)
def handle_api_error(error):
    return output_json(error.to_dict(), error.code)


map_user(api)
map_status(api)
map_article(api)
map_poem(api)
map_other(api)

#api.add_resource(Authorizations, '/authorizations')
#api.add_resource(VerifyCodes, '/verifycodes')
#api.add_resource(UserFollowers, '/users/<id>/followers')
#api.add_resource(UserFolloweds, '/users/<id>/followeds')
#api.add_resource(StatusesRes, '/statuses')
#api.add_resource(StatusRes, '/statuses/<id>')
#api.add_resource(UserStatusesRes, '/users/<user_id>/statuses')
#api.add_resource(StatusLikesRes, '/statuses/<id>/likes')
#api.add_resource(UserStatusLikesRes, '/users/<id>/likes/statuses')
#api.add_resource(ArticleSpiderRes, '/articles/spider')
#api.add_resource(ArticlesRes, '/articles')
#api.add_resource(ArticleRes, '/articles/<id>')
#api.add_resource(SourcesRes, '/sources')
#api.add_resource(SettingsRes, '/settings')
#api.add_resource(SettingWxRes, '/setting/wx')
#api.add_resource(SettingPingRes, '/setting/ping')
#api.add_resource(SpiderArtsRes, '/spiderarts')
#api.add_resource(SpiderArticleRes, '/spider/article')
#api.add_resource(PoemAuthorsRes, '/p/authors')
#api.add_resource(PoemsRes, '/p/poems')
#api.add_resource(PoemTagsRes, '/p/tags')
#api.add_resource(QiniuTokenRes, '/qiniu/token')
#api.add_resource(QingAuthRes, '/qing/token')
#api.add_resource(FeedbackRes, '/feedbacks/<id>')
#api.add_resource(FeedbacksRes, '/feedbacks')
#api.add_resource(UserFeedbackRes, '/users/<id>/feedbacks')
#api.add_resource(SettingWxMiniRes, '/wx_mini')
#api.add_resource(ApiLogRes, '/logs')
#api.add_resource(StatusShieldsRes, '/statuses/<id>/shield')
#api.add_resource(TopicsRes, '/topics')
#api.add_resource(TopicStatusesRes, '/topics/<id>/statuses')
#api.add_resource(TopicUsersRes, '/topics/<id>/users')
#api.add_resource(UserTopicsRes, '/users/<id>/topic
#api.add_resource(UserTopicJoinsRes, '/users/<id>/topics/joins')
#api.add_resource(TagsRes, '/tags')
#api.add_resource(TagRes, '/tags/<id>')
#api.add_resource(ArticleTagsRes, '/articles/<id>/tags')
#api.add_resource(ProductsRes, '/products')
#api.add_resource(ProductRes, '/products/<id>')
#api.add_resource(ProductVersionsRes, '/products/<id>/versions')
#api.add_resource(VersionRes, '/versions/<id>')

if __name__ == '__main__':
#    app.run(debug=True)
    app.run(debug=True, host="192.168.0.23", port=5000)


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.access')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
