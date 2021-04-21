# coding=utf-8
# author:xs
from flask import request, g
from flask_restful import reqparse, Resource
from instance.errors import *
from instance.im163 import createIMChatRoom 
from instance.utils import output_json, login_required

parser = reqparse.RequestParser()
_args = ['room_name']
for _arg in _args:
    parser.add_argument(_arg)


class IMChatRoomsRes(Resource):

    @login_required
    def post(self):
        args = parser.parse_args()
        room_name = args.get('room_name')
        if not room_name:
            raise MissingRequiredParameter(['room_name'])
        ok, data = createIMChatRoom(g.user_id, room_name)
        if ok:
            return {"room_id": data}
        
        return output_json('', 500, error=data) 


