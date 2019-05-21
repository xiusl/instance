# coding=utf-8
# author:xsl

from flask import Flask, current_app
from flask_restful import Api

from instance.utils import output_json
from instance.resource import Users
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


@app.errorhandler(ApiBaseError)
def handle_api_error(error):
    return output_json(error.to_dict(), error.code)


api.add_resource(Users, '/users')


if __name__ == '__main__':
    app.run()




