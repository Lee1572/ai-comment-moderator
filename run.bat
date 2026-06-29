@echo off
echo 
echo  Starting AI Comment Moderator
echo 
echo.

:: Check if virtual environment exists
if not exist "venv" (
    echo [ERROR] Virtual environment not found.
    echo Please run setup.bat first.
    pause
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Check if .env exists
if not exist ".env" (
    echo [WARNING] .env file not found.
    echo Please create .env with your OPENAI_API_KEY
    echo Copy .env.example to .env and add your key
    echo.
)

:: Run the application
echo [INFO] Starting Flask server...
echo Server will run on http://localhost:5000
echo Press Ctrl+C to stop
echo.
python app.py

pause