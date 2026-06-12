#!/bin/bash

mkdir -p /tmp/simple_django && chmod 777 /tmp/simple_django

docker run \
    -v /tmp/simple_django:/data \
    -v /etc/simple_django/litestream.yml:/etc/litestream.yml \
    litestream/litestream restore /data/db.sqlite3

cp /tmp/simple_django/db.sqlite3 /var/simple_django/db.sqlite3

chown -R simple_django:simple_django /var/simple_django/db.sqlite3