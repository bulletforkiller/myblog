#!/bin/bash

# activate the virtual environment
source /home/myblog/dj_env/bin/activate

# stop nginx
nginx -s stop

# stop uwsgi
uwsgi --stop /home/myblog/uwsgi_file/uwsgi.pid

# stop database and redis
docker stop my_pg
docker stop my_redis
