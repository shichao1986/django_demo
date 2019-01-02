# 本docker image内部已经安装了django，nginx，uwsgi，supervisor等一系列相关应用
# 本docker file示范如何通过docker将项目部署为自启动
FROM django-demo:latest

ENV PROJECT_DIR = '/home/cyuser/django_demo'

WORKDIR /home/cyuser/django_demo

# copy project
# COPY /home/cyuser/sc_dev/django_demo/ /home/cyuser/django_demo

COPY docker/django_demo_supervisor.conf /etc/supervisor/conf.d/django_demo_supervisor.conf
COPY docker/nginx_supervisor.conf /etc/supervisor/conf.d/nginx_supervisor.conf

ENTRYPOINT ["supervisord -c /home/cyuser/django_demo/DjangoDemoProj/docker/supervisord.conf"]

