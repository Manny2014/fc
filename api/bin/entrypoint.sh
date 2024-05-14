#!/bin/bash

gunicorn -w 2 "payments.app:create_app()" --bind "0.0.0.0:${APP_PORT}" --timeout 90