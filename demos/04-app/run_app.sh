#!/bin/bash

# Set default environment variables
export PORT=${PORT:-8081}
export DEBUG=${DEBUG:-false}

# Print configuration
echo "Starting Hello-GenAI Python application"
echo "Port: $PORT"
echo "Debug mode: $DEBUG"

# Run the application
python app.py
