#!/bin/bash

# THIS FILE WILL BE REPLACE BY A ROBUST DOCKER CONFIG

# Get the absolute path
ABS_PATH=$(pwd)

# Activate Python environment and execute backend commands
source "$ABS_PATH/my_new_env/bin/activate"

# Run backend setup commands
cd backend
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py crontab add
python3 manage.py runserver 9000