#!/bin/bash

echo "Start the server (Debug Mode)......."
FLASK_APP=main.py FLASK_DEBUG=1 python -m flask run