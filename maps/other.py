# coding=utf-8
# author:xsl

from instance.maps import mapping
from instance.resource import (
    ApiLogRes,
    VerifyCodes,
    Authorizations,

    SettingsRes,
    SettingWxRes,
    SettingPingRes,
    SettingWxMiniRes,

    QiniuTokenRes,
    QingAuthRes,

    ProductsRes,
    ProductRes,
    ProductVersionsRes,
    VersionRes,

    IMChatRoomsRes,

    FeedbackRes,
    FeedbacksRes,

    ArticleSpiderRes,
)

other_map = {
    ApiLogRes: '/logs',
    VerifyCodes: '/verifycodes',
    Authorizations: '/authorizations',

    SettingsRes: '/settings',
    SettingWxRes: '/setting/wx',
    SettingPingRes: '/setting/ping',
    SettingWxMiniRes: '/wx_mini',

    QiniuTokenRes: '/qiniu/token',
    QingAuthRes: '/qing/token',

    ProductsRes: '/products',
    ProductRes: '/products/<id>',
    ProductVersionsRes: '/products/<id>/versions',
    VersionRes: '/versions/<id>',

    IMChatRoomsRes: '/im/chatrooms',

    FeedbackRes: '/feedbacks/<id>',
    FeedbacksRes: '/feedbacks',

    # fix old app
    ArticleSpiderRes: '/articles/spider',
}

def map_other(api):
    mapping(api, '', other_map)
