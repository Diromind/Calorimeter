#!/bin/bash

echo "Starting install process for 'server' module"

sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib

PROJECT_DIR="$HOME/calorimeter"
if [ ! -d "$PROJECT_DIR" ]; then
    sudo mkdir -p "$PROJECT_DIR"
    sudo chown $USER:$USER "$PROJECT_DIR"
fi
cd "$PROJECT_DIR" || exit

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install fastapi uvicorn[standard] aiogram>3.0.0 aiohttp asyncpg python-dotenv psycopg2-binary yaml

echo "Installation for 'server' module completed successfully!"
