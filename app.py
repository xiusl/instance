# coding=utf-8
# author:xsl

from flask import Flask, g, current_app, request
from flask_restful import Api

#import settings
from instance.models import User
from instance.utils import output_json
from instance.resource import (
    StatusesRes, 
    StatusRes, 
    Authorizations, 
    UsersRes, 
    UserRes,
    VerifyCodes, 
    UserFollowers
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


@app.before_request
def before_request():
    token = request.headers.get("X-Token")
    g.user = None
    if token:
        u = User.get_by_token(token)
        g.user = u

@app.errorhandler(ApiBaseError)
def handle_api_error(error):
    return output_json(error.to_dict(), error.code)

api.add_resource(Authorizations, '/authorizations')
api.add_resource(UsersRes, '/users')
api.add_resource(UserRes, '/users/<id>')
api.add_resource(VerifyCodes, '/verifycodes')
api.add_resource(UserFollowers, '/users/<id>/followers')
api.add_resource(StatusesRes, '/statuses')
api.add_resource(StatusRes, '/statuses/<id>')

if __name__ == '__main__':
    app.run()




