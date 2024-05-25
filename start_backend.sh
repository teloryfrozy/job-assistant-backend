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

# Function to install Docker on WSL (Linux)
install_docker_wsl() {
    print_message $BLUE "Installing Docker on WSL..."
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
}

# Ensure Docker daemon is running
print_message $YELLOW "Starting Docker daemon using service command..."
sudo service docker start

# Check if Docker daemon is running
if ! sudo service docker status >/dev/null 2>&1; then
    print_message $RED "Docker daemon is not running. Please start the Docker daemon."
    exit 1
fi

# Check if Docker is installed
if ! command -v docker >/dev/null 2>&1; then
    install_docker_wsl
else
    print_message $GREEN "Docker is already installed."
fi

# Check if Docker Compose is installed
if ! command -v docker-compose >/dev/null 2>&1; then
    print_message $YELLOW "Docker Compose not found. Installing Docker Compose..."
    sudo apt-get install docker-compose-plugin -y
else
    print_message $GREEN "Docker Compose is already installed."
fi

# Add user to Docker group if not already a member
if ! groups $USER | grep -q '\bdocker\b'; then
    print_message $YELLOW "Adding user to Docker group..."
    sudo usermod -aG docker $USER
    print_message $YELLOW "Please log out and log back in for the changes to take effect."
    exit 1
fi

# Run Docker Compose
print_message $BLUE "Starting Docker Compose"
docker-compose -p job_assistant up --build