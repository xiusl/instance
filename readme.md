### instance api

- 哩嗑 App 接口代码
- Flask + Flask_Restful + mongoengine
- 线上地址：https://ins-api.sleen.top
- [Wiki](https://github.com/xiusl/instance/wiki)
- No gank!!! Thank you!!!

```
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
```
