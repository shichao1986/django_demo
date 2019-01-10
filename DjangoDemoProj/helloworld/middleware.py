# coding:utf-8

# 自定义django中间件，本中间件用于限制单一账户重复登陆，
# 以及检查单一账户短时间内多次登录
# 本例会使用redis作为辅助工具，redis的配置优化不在本例的考虑范围
# 使用redis存储当前账户登录时产生的最新的session_key值，并将之前的session从db中删除
# 从而达到失效更早的登录的效果
# django 中间件的自定义请参考连接https://blog.csdn.net/qq_41964425/article/details/83060648

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.contrib.sessions.backends.db import SessionStore
import redis

REDIS_HOST = '10.6.3.29'
REDIS_PORT = 16379

pool = redis.BlockingConnectionPool(max_connections=10, host=REDIS_HOST, port=REDIS_PORT)

# 事实上使用中间件防止重复登录的方法效率名不是最好，但是却更安全
# 另一种效率更好的方式是只要在用户登录的接口内对redis内的值进行维护即可
class UserLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.session is not None and request.session.get('_auth_user_id', None) is not None:
            try:
                r = redis.Redis(connection_pool=pool)
                user_str = 'user_session_key_{}'.format(request.session['_auth_user_id'].zfill(10))
                if r.exists(user_str):
                    last_session_key = r.get(user_str).decode()
                    if last_session_key != request.session.session_key:
                        r.set(user_str, request.session.session_key)
                        # delete session in db
                        last_session = SessionStore(last_session_key)
                        last_session.delete()
                else:
                    r.set(user_str, request.session.session_key)
            except Exception as e:
                # 之前的session已经被删除掉
                pass

    def process_response(self, request, response):
        if request.session is not None and request.session.get('_auth_user_id', None) is not None:
            try:
                r = redis.Redis(connection_pool=pool)
                user_str = 'user_session_key_{}'.format(request.session['_auth_user_id'].zfill(10))
                if r.exists(user_str):
                    last_session_key = r.get(user_str).decode()
                    if last_session_key != request.session.session_key:
                        r.set(user_str, request.session.session_key)
                        # delete session in db
                        last_session = SessionStore(last_session_key)
                        last_session.delete()
                else:
                    r.set(user_str, request.session.session_key)
            except Exception as e:
                # 之前的session已经被删除掉
                pass

        return response