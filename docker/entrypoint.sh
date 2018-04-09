#!/bin/sh

cd /opt/arsenal-c2/
uwsgi --ini uwsgi.ini --lazy-apps --daemonize /var/log/arsenal-c2.log
nginx -g "daemon off;"
