#!/bin/sh
echo "Starting forecast_agent..."
python forecast_agent.py
echo "Removing duplicates..."
python Duplicate_removal.py
echo "Starting FastAPI server..."
uvicorn forecast_api:app --host 0.0.0.0 --port 8000
