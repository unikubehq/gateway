#!/usr/bin/env sh

case "$RUN_ENV" in
  dev)    python /app/main.py ;;
  web)    python /app/main.py ;;
esac
