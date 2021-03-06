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
from django.http import HttpResponse
import redis
import threading
import datetime
import logging

REDIS_HOST = '10.6.3.29'
REDIS_PORT = 16379

# 此时间为session的有效时间+1 分钟，设定redis过期时间，节省redis空间
EXPIRE_TIME = settings.SESSION_COOKIE_AGE + 60

# 10秒100次
FAST_ACCESS_THRESHHOLD = 100
FAST_ACCESS_INTERVAL = 10
FAST_ACCESS_FORBIDDEN = 60
ACL_BLACK_LIST = 'acl_black_list'

MULTIPLE_LOGIN_THRESHHOLD = 5
MULTIPLE_LOGIN_INTERVAL = 15
# 15分钟禁止该用户访问
MULTIPLE_LOGIN_FORBIDDEN = 60 * 15
MULTIPLE_LOGIN_USER = 'multiple_login_user'

pool = redis.BlockingConnectionPool(max_connections=10, host=REDIS_HOST, port=REDIS_PORT)

logger = logging.getLogger('helloworld.middleware')

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
    # 事实上ip禁止应该交由更早的服务去实现，例如nginx
    def process_request(self, request):
        try :
            r = redis.Redis(connection_pool=pool)
            ip_key = '{}/{}'.format(ACL_BLACK_LIST, request.META['REMOTE_ADDR'])
            if r.exists(ip_key):
                return HttpResponse('该IP短时间内访问过于频繁', status=401)
        except Exception as e:
            print(e)

        return None

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
            r.set(user_str, request.session.session_key, ex=EXPIRE_TIME)
            # delete session in db
            last_session = SessionStore(last_session_key)
            last_session.delete()
        return

    def _check_multiple_login(self, r, request):
        user_login_key = '{}:{}'.format(MULTIPLE_LOGIN_USER, request.session['_auth_user_id'].zfill(10))
        while True:
            times = r.get(user_login_key)
            if times is None:
                # key 不存在时初始化定时器
                if r.set(user_login_key, 1, nx=True, ex=MULTIPLE_LOGIN_INTERVAL):
                    logger.debug('init {} 1'.format(user_login_key))
                    break
                    # 设置失败则重新获取key值
            else:
                # 获取key值检测次数，小于阈值+1，大于阈值添加黑名单
                times = int(times)
                if times < MULTIPLE_LOGIN_THRESHHOLD - 1:
                    logger.debug('{}:incr 1'.format(user_login_key))
                    r.incr(user_login_key, 1)
                else:
                    ip_key = '{}/{}'.format(ACL_BLACK_LIST, request.META['REMOTE_ADDR'])
                    r.set(ip_key, 1, ex=MULTIPLE_LOGIN_FORBIDDEN)
                    logger.debug('add ip {} to black list'.format(request.META['REMOTE_ADDR']))
                break

    def process_response(self, request, response):
        if request.session is not None and request.session.get('_auth_user_id', None) is not None:
            # 限制多点登录
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

                            # 此处增加用户多点登录频率检查，防止用户频繁多点登录
                            # 保护频繁被踢下线的账户的安全
                            self._check_multiple_login(r, request)
                        break
                    else:
                        # 此分支失败，则说明发生并发登录，即同一账户在不同处同时登录，
                        # 后登录者再此执行踢掉之前登录者即可
                        if r.set(user_str, request.session.session_key, nx=True, ex=EXPIRE_TIME):
                            break
            except Exception as e:
                # 之前的session已经被删除掉
                logger.error(e)
                pass

            # 限制短时间内的访问次数，大于阈值时将用户IP增加到黑名单
            # 该黑名单应该存在一定的失效时间，而且应该尽量早的限制访问
            # 本例为了起到说明的作用所以仅将检查放在UserLoginMiddleware.process_request中
            # 本检查只能限制用户在一次登录成功后的访问次数，对于用户频繁的重新登录则无法检查
            # 因为数据保存在了session中，重新登录后session会更新
            if request.session.get('fast_access_start_time', None) is None:
                request.session['fast_access_start_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                request.session['fast_access_count'] = 1
                logger.debug('fast_access init:{} - {}'.format(request.session['fast_access_start_time'],
                                                               request.session['fast_access_count']))
            else:
                request.session['fast_access_count'] += 1
                logger.debug('fast_access_count add 1 = {}'.format(request.session['fast_access_count']))
                if request.session['fast_access_count'] > FAST_ACCESS_THRESHHOLD:
                    nowtime = datetime.datetime.now()
                    starttime = datetime.datetime.strptime(request.session['fast_access_start_time'], '%Y-%m-%d %H:%M:%S')
                    if (nowtime - starttime).seconds <= FAST_ACCESS_INTERVAL:
                        ip_key = '{}/{}'.format(ACL_BLACK_LIST, request.META['REMOTE_ADDR'])
                        r.set(ip_key, 1, ex=FAST_ACCESS_FORBIDDEN)
                        logger.debug('add ip {} to black list'.format(request.META['REMOTE_ADDR']))

                    del request.session['fast_access_start_time']



        return response