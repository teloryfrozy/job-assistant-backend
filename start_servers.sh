#!/bin/bash

# Start PostgreSQL
# sudo service postgresql start

# Get the absolute path
ABS_PATH=$(pwd)

# Activate Python environment and execute backend commands
source "$ABS_PATH/backend/py_env/bin/activate"

# Run backend setup commands
cd backend/JobAssistant
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 9000 &  # Run the backend server in the background

# Move to the frontend directory, install dependencies, and start the server
cd ../frontend
# Here put all the commands to start React server
# npm run serve (Vue.js)