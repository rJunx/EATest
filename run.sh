#!/bin/bash

echo "Start the server (Normal Mode)......."
#FLASK_APP=./EATest/main.py flask run

cd EATest
gunicorn main:app -w 4 -b 127.0.0.1:5000 -k gevent