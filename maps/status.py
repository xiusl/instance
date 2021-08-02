# coding=utf-8
# author:xsl

from instance.maps import mapping
from instance.resource import (
    StatusesRes,
    StatusRes,
    StatusLikesRes,
    StatusShieldsRes,
    TopicsRes,
    TopicStatusesRes,
    TopicUsersRes,
)

status_prefix = '/statuses'
status_map = {
    StatusesRes: '',
    StatusRes: '/<id>',
    StatusLikesRes: '/<id>/likes',
    StatusShieldsRes: '/<id>/shield',
}

topic_prefix = '/topics'
topic_map = {
    TopicsRes: '',
    TopicStatusesRes: '/<id>/statuses',
    TopicUsersRes: '/<id>/users',
}

def map_status(api):
    mapping(api, status_prefix, status_map)
    mapping(api, topic_prefix, topic_map)
