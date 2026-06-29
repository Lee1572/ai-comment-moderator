@echo off
echo 
echo  AI Comment Moderator Setup (Windows)
echo 
echo.

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

:: Check Python version
python -c "import sys; exit(0 if sys.version_info >= (3,8) else 1)"
if %errorlevel% neq 0 (
    echo [ERROR] Python 3.8 or higher is required.
    echo Current version:
    python --version
    pause
    exit /b 1
)

:: Check if git is installed
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] Git is not installed or not in PATH.
    echo You can still run the project but won't be able to use Git.
    echo Install Git from https://git-scm.com
    echo.
)

:: Initialize Git repository if not exists
if not exist ".git" (
    echo [INFO] Initializing Git repository...
    git init 2>nul
)

:: Create virtual environment
echo [INFO] Creating Python virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)

:: Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

:: Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

:: Install dependencies
echo [INFO] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

:: Install development dependencies
echo [INFO] Installing development dependencies...
pip install -r requirements-dev.txt

:: Create .env file if it doesn't exist
if not exist ".env" (
    echo [INFO] Creating .env file from example...
    copy .env.example .env
    echo.
    echo [WARNING] Please add your OPENAI_API_KEY to the .env file!
    echo.
)

:: Create necessary directories
if not exist "tests" mkdir tests
if not exist "docs" mkdir docs

:: Create initial test files if they don't exist
if not exist "tests\__init__.py" (
    echo # Test package > tests\__init__.py
)
if not exist "tests\test_app.py" (
    echo # Test app > tests\test_app.py
)
if not exist "tests\test_moderator.py" (
    echo # Test moderator > tests\test_moderator.py
)

:: Create moderation log
if not exist "moderation_log.json" (
    echo [] > moderation_log.json
)

:: Create README if it doesn't exist
if not exist "README.md" (
    echo # AI Comment Moderator > README.md
    echo. >> README.md
    echo A REST API for AI-powered comment moderation with appeal system. >> README.md
)

:: Initial Git commit
if exist ".git" (
    echo [INFO] Creating initial Git commit...
    git add .
    git commit -m "Initial commit: AI Comment Moderator with Appeal System" 2>nul
)

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Add your OPENAI_API_KEY to .env file
echo 2. Activate the virtual environment:
echo    venv\Scripts\activate
echo 3. Run the server:
echo    python app.py
echo 4. To use Git:
echo    git remote add origin https://github.com/yourusername/repo.git
echo    git push -u origin main
echo.
pause