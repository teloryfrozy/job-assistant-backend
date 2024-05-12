#!/bin/bash

# Start PostgreSQL
# sudo service postgresql start

# Get the absolute path
ABS_PATH=$(pwd)

# Activate Python environment and execute backend commands
source "$ABS_PATH/py_env/bin/activate"

# Run backend setup commands
cd backend
python3 manage.py makemigrations
python3 manage.py migrate
python manage.py crontab add
python3 manage.py runserver 9000  # Run the backend server in the background