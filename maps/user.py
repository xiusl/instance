# coding=utf-8
# author:xsl

from instance.maps import mapping
from instance.resource import (
    UsersRes,
    UserRes,
    UserPasswordRes,
    UserFollowers,
    UserFolloweds,
    UserStatusesRes,
    UserStatusLikesRes,
    UserFeedbackRes,
    UserTopicsRes,
    UserTopicJoinsRes,
)

user_prefix = '/users'
user_map = {
    UsersRes: '',
    UserRes: '/<id>',
    UserPasswordRes: '/<id>/password',
    UserFollowers: '/<id>/followers',
    UserFolloweds: '/<id>/followeds',
    UserStatusesRes: '/<user_id>/statuses',
    UserStatusLikesRes: '/<id>/likes/statuses',
    UserFeedbackRes: '/<id>/feedbacks',
    UserTopicsRes: '/<id>/topics',
    UserTopicJoinsRes: '/<id>/topics/joins',
}

def map_user(api):
    mapping(api, user_prefix, user_map)
