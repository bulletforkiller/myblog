#!/bin/bash

# start database and redis
docker start my_pg
docker start my_redis

# activate the virtual environment
source /home/myblog/dj_env/bin/activate

# run uwsgi
uwsgi --ini /home/myblog/uwsgi_file/uwsgi.ini

# start nginx
nginx
