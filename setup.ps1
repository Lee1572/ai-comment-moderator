# AI Comment Moderator Setup Script (Windows PowerShell)
# Run with: powershell -ExecutionPolicy Bypass -File setup.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " AI Comment Moderator Setup (Windows)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Python is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Python version
$pythonVersionCheck = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
if ([version]$pythonVersionCheck -lt [version]"3.8") {
    Write-Host "[ERROR] Python 3.8 or higher is required." -ForegroundColor Red
    Write-Host "Current version: $pythonVersionCheck" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Git is installed
try {
    $gitVersion = git --version 2>&1
    Write-Host "[OK] Git found: $gitVersion" -ForegroundColor Green
    $gitAvailable = $true
}
catch {
    Write-Host "[WARNING] Git is not installed or not in PATH." -ForegroundColor Yellow
    Write-Host "Install Git from https://git-scm.com" -ForegroundColor Yellow
    $gitAvailable = $false
}

# Initialize Git repository
if (-not (Test-Path ".git")) {
    if ($gitAvailable) {
        Write-Host "[INFO] Initializing Git repository..." -ForegroundColor Yellow
        git init
    }
}

# Create virtual environment
Write-Host "[INFO] Creating Python virtual environment..." -ForegroundColor Yellow
python -m venv venv
if (-not (Test-Path "venv")) {
    Write-Host "[ERROR] Failed to create virtual environment." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate virtual environment
Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "[INFO] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "[INFO] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to install dependencies." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Install development dependencies
Write-Host "[INFO] Installing development dependencies..." -ForegroundColor Yellow
pip install -r requirements-dev.txt

# Create .env file
if (-not (Test-Path ".env")) {
    Write-Host "[INFO] Creating .env file from example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host ""
    Write-Host "[WARNING] Please add your OPENAI_API_KEY to the .env file!" -ForegroundColor Red
    Write-Host ""
}

# Create necessary directories
$directories = @("tests", "docs")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "[INFO] Created directory: $dir" -ForegroundColor Yellow
    }
}

# Create initial test files
$testFiles = @{
    "tests\__init__.py"       = "# Test package"
    "tests\test_app.py"       = "# Test app"
    "tests\test_moderator.py" = "# Test moderator"
}

foreach ($file in $testFiles.Keys) {
    if (-not (Test-Path $file)) {
        $content = $testFiles[$file]
        $content | Out-File -FilePath $file -Encoding UTF8
        Write-Host "[INFO] Created file: $file" -ForegroundColor Yellow
    }
}

# Create moderation log
if (-not (Test-Path "moderation_log.json")) {
    "[]" | Out-File -FilePath "moderation_log.json" -Encoding UTF8
    Write-Host "[INFO] Created moderation_log.json" -ForegroundColor Yellow
}

# Create README if it doesn't exist
if (-not (Test-Path "README.md")) {
    @"
# AI Comment Moderator

A REST API for AI-powered comment moderation with appeal system.

## Quick Start
1. Add your OPENAI_API_KEY to .env file
2. Run: python app.py
3. Server runs on http://localhost:5000
"@ | Out-File -FilePath "README.md" -Encoding UTF8
}

# Initial Git commit
if ($gitAvailable -and (Test-Path ".git")) {
    Write-Host "[INFO] Creating initial Git commit..." -ForegroundColor Yellow
    git add .
    git commit -m "Initial commit: AI Comment Moderator with Appeal System" 2>&1 | Out-Null
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Add your OPENAI_API_KEY to .env file" -ForegroundColor White
Write-Host "2. Activate the virtual environment:" -ForegroundColor White
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "3. Run the server:" -ForegroundColor White
Write-Host "   python app.py" -ForegroundColor Cyan
Write-Host "4. To use Git:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/yourusername/repo.git" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to exit"