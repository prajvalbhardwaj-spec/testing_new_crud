#!/bin/bash
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Seeding database..."
python seed.py

echo "Starting server..."
python -m uvicorn main:app --reload
