#!/bin/sh

docker run --name my_pg -p 127.0.0.1:5432:5432 \
-v /home/pg_data:/var/lib/postgresql/data \
-d postgres