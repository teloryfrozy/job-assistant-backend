#!/bin/sh

# ────────────────────────────────────────────────────────────────────────────────
# Shell Script for Django Application Setup and Cron Management
# ────────────────────────────────────────────────────────────────────────────────

# Define color codes
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
NC='\033[0m' # No Color

print_message() {
    echo "${1}${2}${NC}"
}

# Apply database migrations
print_message $BLUE "Applying database migrations..."
python3 manage.py migrate && \
    print_message $GREEN "Migrations applied successfully." || \
    { print_message $RED "Migrations failed."; exit 1; }

# Start Cron service
print_message $BLUE "Starting Cron service..."
service cron start

# Set cron tasks
print_message $BLUE "Setting cron tasks..."
python3 manage.py crontab add && \
    print_message $GREEN "Cron tasks set successfully." || \
    { print_message $RED "Setting cron tasks failed."; exit 1; }

# Show active cron jobs
print_message $YELLOW "Active cron jobs:"
python3 manage.py crontab show

# Start Django application
print_message $BLUE "Starting Django application..."
exec "$@"