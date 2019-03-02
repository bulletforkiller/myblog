#!/bin/sh

docker run -p 127.0.0.1:6379:6379 \
-v /home/myblog/docker/redis/data:/data:rw \
-v /home/myblog/docker/redis/redis.conf:/etc/redis/redis.conf:ro \
--privileged=true \
--name my_redis \
-d redis redis-server /etc/redis/redis.conf