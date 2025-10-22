#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Check if virtual environment exists, if not create it and install dependencies
if [ ! -d "venv" ]; then
    echo "Creating virtual environment in 'venv' for the first time..."
    python3 -m venv venv
    echo "Installing dependencies from requirements.txt..."
    source venv/bin/activate
    pip install -r requirements.txt
    echo "Setup complete!"
else
    echo "Virtual environment already exists. Skipping setup."
fi

# Activate the virtual environment and run the application
echo "Activating virtual environment and starting the application..."
source venv/bin/activate
python run.py
