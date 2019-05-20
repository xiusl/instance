# coding=utf-8
# author:xsl

from flask import Flask
from flask_restful import Api

from instance.utils import output_json
from instance.resource import Users

class MyApi(Api):

    def __init__(self, *args, **kwargs):
        super(MyApi, self).__init__(*args, **kwargs)
        self.representations = {
            'application/json': output_json,
        }

    def handle_error(self, e):
        
    

app = Flask(__name__)
api = MyApi(app, catch_all_404s=True)




api.add_resource(Users, '/users')


if __name__ == '__main__':
    app.run()




