#Flask minor details.

- `flask_login`
- `from flask_login import UserMixin, AnonymousUserMixin`


``` 
login_manager.anonymous_user=AnonymousUser
class AnonymousUser(AnonymousUserMixin):
```


- `from flask_login import login_manager`
- `db.event.listen(Post.body,'set',Post.on_changed_body)`

>  - 问题是这里为什么要放在model里. 'set'是干啥的。 Post.on_changed_body显然是调用这个动作。

-------

- bleach, markdown 

```
bleach.linkify(bleach.clean(markdown(value,output_format='html'),tags=allowd_tags,strip=True))
```
- datetime.utcnow
- flask.make_response
- flask_login.current_user
- flask_login.login_required

> current_user._get_current_object() 得到当前user.
> 问 current_user 是怎么被选定的呢？

- flask.request
    - request.cookies
    - request.args.get('page',1,type=int')
- flask.abort(403)
- 

