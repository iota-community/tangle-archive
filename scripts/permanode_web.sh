#!/usr/bin/env bash

NAME="permanode"
WORKERS=2
WORKER_CLASS=eventlet
TIMEOUT=120

echo "Starting $NAME"

python app.py sync

exec gunicorn app:app -b 0.0.0.0:9080 \
  --reload \
  --name $NAME \
  --workers $WORKERS \
  --timeout $TIMEOUT \
  --worker-class $WORKER_CLASS
