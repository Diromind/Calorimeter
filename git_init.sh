#!/bin/bash

# Use this script to copy repo to local pod
# After that use modules install scripts to proceed

sudo apt update && sudo apt install -y git

read -p "Enter your Git repository URL: " REPO_URL
PROJECT_DIR="$HOME/calorimeter"
if [ -d "$PROJECT_DIR" ]; then
    echo "Directory $PROJECT_DIR already exists. Exiting..."
    exit 1
fi

git clone "$REPO_URL" "$PROJECT_DIR"
echo "Repository cloned into $PROJECT_DIR"