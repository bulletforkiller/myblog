#!/bin/bash

source /home/myblog/dj_env/bin/activate
uwsgi --ini /home/myblog/uwsgi_file/uwsgi.ini
