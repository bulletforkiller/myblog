#!/bin/bash

# some var
uwsgi_config=/home/myblog/uwsgi_file/uwsgi.ini

# activate the virtual environment
source /home/myblog/dj_env/bin/activate

# flash the website, just flash uwsgi
uwsgi --stop $uwsgi_config
uwsgi --ini $uwsgi_config