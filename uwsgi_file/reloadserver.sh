#!/bin/bash

# activate the virtual environment
source /home/myblog/dj_env/bin/activate

# reload uwsgi
uwsgi --reload /home/myblog/uwsgi_file/uwsgi.ini