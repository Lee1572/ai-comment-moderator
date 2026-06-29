#!/bin/bash
# Run script for Unix/Linux/Mac

echo 
echo  Starting AI Comment Moderator"
echo 
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[ERROR] Virtual environment not found."
    echo "Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "[WARNING] .env file not found."
    echo "Please create .env with your OPENAI_API_KEY"
    echo "Copy .env.example to .env and add your key"
    echo ""
fi

# Run the application
echo "[INFO] Starting Flask server..."
echo "Server will run on http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""
python app.py