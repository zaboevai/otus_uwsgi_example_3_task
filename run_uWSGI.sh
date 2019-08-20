#!/usr/bin/env bash

uwsgi --http :8000 --wsgi-file wsgi_server.py --master --die-on-term --stats 127.0.0.1:9191
