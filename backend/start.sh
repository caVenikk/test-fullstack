#!/bin/bash

uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload &

# Start the bot
python3 src/bot/main.py
