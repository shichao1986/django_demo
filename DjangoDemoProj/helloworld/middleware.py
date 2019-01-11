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
import threading

REDIS_HOST = '10.6.3.29'
REDIS_PORT = 16379

pool = redis.BlockingConnectionPool(max_connections=10, host=REDIS_HOST, port=REDIS_PORT)

def sychronized(func):
    if not hasattr(func, '_t_lock'):
        func._t_lock = threading.Lock()
    def inner(*argv, **kwargs):
        with func._t_lock:
            return func(*argv, **kwargs)

    return inner

# 事实上使用中间件防止重复登录的方法效率名不是最好，但是却更安全
# 另一种效率更好的方式是只要在用户登录的接口内对redis内的值进行维护即可
class UserLoginMiddleware(MiddlewareMixin):
    # def process_request(self, request):
    #     if request.session is not None and request.session.get('_auth_user_id', None) is not None:
    #         try:
    #             r = redis.Redis(connection_pool=pool)
    #             user_str = 'user_session_key_{}'.format(request.session['_auth_user_id'].zfill(10))
    #             if r.exists(user_str):
    #                 last_session_key = r.get(user_str).decode()
    #                 if last_session_key != request.session.session_key:
    #                     r.set(user_str, request.session.session_key)
    #                     # delete session in db
    #                     last_session = SessionStore(last_session_key)
    #                     last_session.delete()
    #             else:
    #                 r.set(user_str, request.session.session_key)
    #         except Exception as e:
    #             # 之前的session已经被删除掉
    #             pass

    @sychronized
    def _update_current_session_key(self, r, request, user_str):
        '''
        本函数线程安全，django的wsgiserver是多线程的，当多个请求并发时此处要使用sychronized装饰器
        :param r:
        :param request:
        :return:
        '''
        # 此处的last_session_key需要重新获取，因为可能被其他线程更新
        last_session_key = r.get(user_str).decode()
        if last_session_key != request.session.session_key:
            r.set(user_str, request.session.session_key)
            # delete session in db
            last_session = SessionStore(last_session_key)
            last_session.delete()
        return

    def process_response(self, request, response):
        if request.session is not None and request.session.get('_auth_user_id', None) is not None:
            try:
                r = redis.Redis(connection_pool=pool)
                user_str = 'user_session_key_{}'.format(request.session['_auth_user_id'].zfill(10))
                while True:
                    if r.exists(user_str):
                        # 此分支只执行一次
                        last_session_key = r.get(user_str).decode()
                        if last_session_key != request.session.session_key:
                            # 仅当session_key不同时才加锁，这使得大部分正常的请求依旧是多线程并发处理
                            # 不会影响系统整体性能
                            self._update_current_session_key(r, request, user_str)
                        break
                    else:
                        # 此分支失败，则说明发生并发登录，即同一账户在不同处同时登录，
                        # 后登录者再此执行踢掉之前登录者即可
                        if r.set(user_str, request.session.session_key, nx=True):
                            break
            except Exception as e:
                # 之前的session已经被删除掉
                pass

        return response