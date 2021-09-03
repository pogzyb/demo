#!/usr/bin/env sh

# `entrypoint.sh` will start the application.
# If running in debug mode, the werkzeug development server is started via the flask cli.
# Otherwise, gunicorn is used to serve the application in production mode.

debug=${FLASK_DEBUG}
if [[ $debug == "0" ]]; then
  echo "Running in production mode."
  gunicorn \
    --workers 1 \
    --threads 4 \
    --bind 0.0.0.0:${PORT} \
    "app:create_app('production')"
else
  echo "Running in non-production mode."
  flask run --host=0.0.0.0 --port=${PORT}
fi
