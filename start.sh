#!/usr/bin/env bash

# Perform any migrations since previously starting
./manage.py migrate

# Start server
./manage.py runserver 0.0.0.0:8000
