#!/bin/bash

if [ "$1" = 'nginx' ]; then
    # Set url
    sed -i "s/{{ANSWER_SERVER}}/$ANSWER_SERVER/g" /etc/nginx/conf.d/default.conf
fi

exec "$@"
