# coding:utf-8

# 自定义django中间件，本中间件用于限制单一账户重复登陆，
# 以及检查单一账户短时间内多次登录
# 本例会使用redis作为辅助工具，redis的配置优化不在本例的考虑范围
# django 中间件的自定义请参考连接https://blog.csdn.net/qq_41964425/article/details/83060648

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.contrib.sessions.backends.db import SessionStore
import redis

REDIS_HOST = '10.6.3.29'
REDIS_PORT = 16379

pool = redis.BlockingConnectionPool(max_connections=10, host=REDIS_HOST, port=REDIS_PORT)

class UserLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.session:
            r = redis.Redis(connection_pool=pool)
            user_str = 'user_session_key_{}'.format(request.session['_auth_user_id'].zfill(10))
            if r.exists(user_str):
                session_key = r.get(user_str)
                if session_key != request.session.session_key:
                    r.set(user_str, session_key)
                    # delete session in db
                    session = SessionStore(session_key)
                    session.delete()
            else:
                r.set(user_str, request.session.session_key)
