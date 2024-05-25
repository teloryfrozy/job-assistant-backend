#!/bin/sh

# Define color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print messages in color
print_message() {
    COLOR=$1
    MESSAGE=$2
    echo "${COLOR}${MESSAGE}${NC}"
}

python3 manage.py migrate
if [ $? -eq 0 ]; then
    print_message $GREEN "Migrations applied successfully."
else
    print_message $RED "Migrations failed."
    exit 1
fi

# Start cron service
print_message $BLUE "Starting Cron service"
service cron start

# Set cron tasks
print_message $BLUE "Setting cron tasks..."
python3 manage.py crontab add
if [ $? -eq 0 ]; then
    print_message $GREEN "Cron tasks set successfully."
else
    print_message $RED "Setting cron tasks failed."
    exit 1
fi

print_message $BLUE "Active cron jobs"
python3 manage.py crontab show

# Start the Django application
print_message $BLUE "Starting Django application"
exec "$@"
