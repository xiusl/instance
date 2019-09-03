# coding=utf-8
# author:xsl

import datetime
from bson import ObjectId
from flask import g
from flask_restful import reqparse, Resource
from instance.errors import BadRequestError, OperationForbiddenError, ResourceDoesNotExist, MissingRequiredParameter
from instance.utils import send_sms_code, login_required
from instance.models import User, UserRelation, UserAction, Status, VerifyCode

parser = reqparse.RequestParser()

_args = ['name', 'phone', 'code', 'password', 'id', 'avatar', 'old_password', 'desc', 'email']
for _arg in _args:
    parser.add_argument(_arg)

class UserRes(Resource):

    def get(self, id):
        if not id:
            raise MissingRequiredParameter(['id'])
        user = User.objects(id=ObjectId(id)).first()
        if not user:
            raise ResourceDoesNotExist()
        c_user = g.user
        if c_user:
            return user.pack(user_id=c_user.id)
        return user.pack()


    @login_required
    def post(self, id):
        if not id:
            raise MissingRequiredParameter(['id'])
        user = User.objects(id=ObjectId(id)).first()
        if not user:
            raise ResourceDoesNotExist()
        if str(user.id) != str(g.user_id):
            raise OperationForbiddenError()
        args = parser.parse_args()
        avatar = args.get('avatar')
        if avatar:
            user.avatar = avatar
        name = args.get('name')
        if name:
            user.name = name
        desc = args.get('desc')
        if desc:
            user.desc = desc
        password = args.get('password')
        flag = False
        if password:
            old_password = args.get('old_password')
            if user.check_passwd(old_password):
                user.password = password
                flag = True
        user.save()
        return user.pack(with_token=flag)
        

class UsersRes(Resource):

    def get(self):
        us = User.objects().limit(10)
        return [u.pack(user_id=g.user_id) for u in us]
    

    def post(self):
        args = parser.parse_args()
        phone = args.get('phone')
        code = args.get('code')
        if not phone or not code:
            raise MissingRequiredParameter(['phone', 'code'])
        vc = VerifyCode.get(phone)
        if int(vc.code) != int(code):
            raise BadRequestError('VerifyCode Error')
        if vc.expired_at < datetime.datetime.now():
            raise BadRequestError('VerifyCode Expired')
        user = User.objects(phone=phone).first()
        if not user:
            user = User()
            user.phone = phone
            user.password = 'Asd110#.'
            user.save()
        return user.pack(with_token=True)



class UserFolloweds(Resource):

    @login_required
    def get(self, id):
        if not id:
            raise MissingRequiredParameter(['id'])
        user = User.objects(id=ObjectId(id)).first()
        if not user:
            raise ResourceDoesNotExist()
        rels = UserRelation.objects(follower_id=user.id).skip(0).limit(10)
        us = [rel.followed_id for rel in rels]
        return list([User.objects(id=uid).first().pack(user_id=g.user_id) for uid in us])


class UserFollowers(Resource):

    @login_required
    def get(self, id):
        if not id:
            raise MissingRequiredParameter(['id'])
        user = User.objects(id=ObjectId(id)).first()
        if not user:
            raise ResourceDoesNotExist()
        rels = UserRelation.objects(followed_id=user.id).skip(0).limit(10)
        us = [rel.follower_id for rel in rels]
        c_user = g.user
        uss = list([User.objects(id=uid).first().pack(user_id=c_user.id) for uid in us])
        return uss


    @login_required
    def post(self, id):
        if not id:
            raise MissingRequiredParameter(['user_id'])
        user = User.objects(id=ObjectId(id)).first()
        if not user:
            raise ResourceDoesNotExist()
        c_user = g.user
        if not c_user.follow(user.id):
            return {"msg": "follow failure"}
        c_user.followed_count += 1
        c_user.save()
        user.following_count += 1
        user.save()
        return user.pack(user_id=c_user.id)

    @login_required
    def delete(self, id):
        if not id:
            raise MissingRequiredParameter(['user_id'])
        user = User.objects(id=ObjectId(id)).first()
        if not user:
            raise ResourceDoesNotExist()
        c_user = g.user
        if not c_user.unfollow(user.id):
            return {"msg": "unfollow failure"}
        c_user.followed_count -= 1
        c_user.save()
        user.following_count -= 1
        user.save()
        return user.pack(user_id=c_user.id)





class Authorizations(Resource):

    def post(self):
        args = parser.parse_args()
        phone = args.get('phone')
        code = args.get('code')
        password = args.get('password')
        if password:
            if not phone:
                raise MissingRequiredParameter(['phone'])
            user = User.objects(phone=phone).first()
            if not user:
                raise ResourceDoesNotExist()
            if not user.check_password(password):
                raise BadRequestError('Password Error')
            return user.pack(with_token=True)

        if not phone or not code:
            raise MissingRequiredParameter(['phone', 'code'])
        vc = VerifyCode.get(phone)
        if int(vc.code) != int(code):
            raise BadRequestError('VerifyCode Error')
        if vc.expired_at < datetime.datetime.now():
            raise BadRequestError('VerifyCode Expired')
        user = User.objects(phone=phone).first()
        if not user:
            user = User()
            user.phone = phone
            user.password = 'Asd110#.'
            user.save()
        return user.pack(with_token=True)

    # reset 17600101706 password
    def get(self):
        u = User.objects(phone="17600101706").first()
        u.password = 'Asd110#.'
        u.save()
        return u.pack()

class VerifyCodes(Resource):

    def get(self):
        args = parser.parse_args()
        phone = args.get('phone')
        if not phone:
            raise MissingRequiredParameter(['phone'])
        vc = VerifyCode.create(phone)
        ok = send_sms_code(phone, vc.code)
        if not ok:
#            vc.delete()
            raise BadRequestError('Send Code Failure.')
        return {'ok': 1}


class UserStatusLikesRes(Resource):

    def get(self, id):
        if not id:
            raise MissingRequiredParameter(['id'])
        u = User.objects(id=ObjectId(id)).first()
        if not u:
            raise ResourceDoesNotExist()
        rels = UserAction.objects(user_id=u.id, action=UserAction.ACTION_LIKE).limit(10)
        status_ids = list([rel.status_id for rel in rels])
        statuses = list([Status.objects(id=ObjectId(s_id)).first().pack(user_id=g.user_id) for s_id in status_ids])
        return statuses


class UserPasswordRes(Resource):
    
    @login_required
    def post(self, id):
        if not id:
            raise MissingRequiredParameter(['id'])
        user = User.objects(id=ObjectId(id)).first()
        if not user:
            raise ResourceDoesNotExist()
        args = parser.parse_args()
        password = args.get('password')
        user.password = password
        user.save()
        return user.pack(with_token=True)


