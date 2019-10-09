### instance api

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

#### auth

- auth

| path | method | params | other |
| --- | --- | --- | --- |
|/authorizations|post|phone,code|null|

- verify code

| path | method | params | other |
| --- | --- | --- | --- |
|/verifycodes|get|phone|null|


#### user

- get one user

| path | method | params | other |
| --- | --- | --- | --- |
|/users/<id\>|get|null|null|


- edit user

| path | method | params | other |
| --- | --- | --- | --- |
|/users/<id\>|post|name,desc,avatar,password,old\_password|need login, change password need old password|


- follow user

| path | method | params | other |
| --- | --- | --- | --- |
|/users/<id\>/followers|post|null|need login|

- unfollow user

| path | method | params | other |
| --- | --- | --- | --- |
|/users/<id\>/followers|delete|null|need login|


- get followers

| path | method | params | other |
| --- | --- | --- | --- |
|/users/<id\>/followers|get|null|need login|

- get followeds

| path | method | params | other |
| --- | --- | --- | --- |
|/users/<id\>/followeds|get|null|need login|


#### status

- get statuses

| path | method | params | other |
| --- | --- | --- | --- |
|/statuses|get|count,page,cursor,direction|null|

- get status by id

| path | method | params | other |
| --- | --- | --- | --- |
|/statuses/<id\>|get|null|null|

- create status

| path | method | params | other |
| --- | --- | --- | --- |
|/statuses|post|content,images|need login|

- edit status

| path | method | params | other |
| --- | --- | --- | --- |
|/statuses/<id\>|post|content,images|need login|

- delete status

| path | method | params | other |
| --- | --- | --- | --- |
|/statuses/<id\>|delete|null|need login|

- get statuses by user

| path | method | params | other |
| --- | --- | --- | --- |
|/users/<user_id\>/statuses|get|count,page,cursor,direction|null|


#### status action

- like status

| path | method | params | other |
| --- | --- | --- | --- |
|/statuses/<id\>/likes|post|null|need login|

- unlike status

| path | method | params | other |
| --- | --- | --- | --- |
|/statuses/<id\>/likes|post|null|need login|


- get users like status

| path | method | params | other |
| --- | --- | --- | --- |
|/statuses/<id\>/likes|get|null|null|


- get statuses by user like

| path | method | params | other |
| --- | --- | --- | --- |
|/users/<user_id\>/like/statuses|get|count,page,cursor,direction|null|


