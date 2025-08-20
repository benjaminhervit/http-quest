#!/bin/bash
# filepath: /Users/benjaminhervit/Documents/Projects/fritids_projekter/http-quest/scripts/kill_port.sh

PORT=${1:-5000}  # Default to port 5000, but allow passing different port

echo "Killing processes on port $PORT..."

# Find and kill processes on the specified port
PIDS=$(lsof -ti:$PORT)

if [ -z "$PIDS" ]; then
    echo "No processes found on port $PORT"
else
    echo "Killing PIDs: $PIDS"
    kill -9 $PIDS
    echo "Done!"
fi