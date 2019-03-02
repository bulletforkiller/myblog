#!/bin/bash

source /home/myblog/dj_env/bin/activate
uwsgi --stop /home/myblog/uwsgi_file/uwsgi.pid
