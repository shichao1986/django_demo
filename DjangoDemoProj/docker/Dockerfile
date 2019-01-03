# 本docker image内部已经安装了django，nginx，uwsgi，supervisor等一系列相关应用
# 本docker file示范如何通过docker将项目部署为自启动
FROM django-demo:latest

ENV PROJECT_DIR="/home/cyuser/DjangoDemoProj"

WORKDIR /home/cyuser

# copy project
COPY DjangoDemoProj ${PROJECT_DIR}

COPY DjangoDemoProj/docker/django_demo_supervisor.conf /etc/supervisor/conf.d/django_demo_supervisor.conf
COPY DjangoDemoProj/docker/nginx_supervisor.conf /etc/supervisor/conf.d/nginx_supervisor.conf
COPY DjangoDemoProj/docker/supervisord.conf /etc/supervisor/supervisord.conf
COPY DjangoDemoProj/docker/nginx.conf /etc/nginx/conf.d/nginx.conf

ENTRYPOINT ["/usr/bin/supervisord"]
CMD ["-n"]

