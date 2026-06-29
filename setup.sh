#!/bin/bash
# AI Comment Moderator Setup Script (Unix/Linux/Mac)

set -e

echo "========================================"
echo " AI Comment Moderator Setup (Unix/Linux)"
echo "========================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH."
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [ "$(printf '%s\n' "3.8" "$PYTHON_VERSION" | sort -V | head -n1)" != "3.8" ]; then
    echo "[ERROR] Python 3.8 or higher is required."
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

echo "[OK] Python $PYTHON_VERSION found"

# Check if Git is installed
if command -v git &> /dev/null; then
    echo "[OK] Git found: $(git --version)"
    GIT_AVAILABLE=true
else
    echo "[WARNING] Git is not installed or not in PATH."
    echo "Install Git from https://git-scm.com"
    GIT_AVAILABLE=false
fi

# Initialize Git repository
if [ ! -d ".git" ] && [ "$GIT_AVAILABLE" = true ]; then
    echo "[INFO] Initializing Git repository..."
    git init
fi

# Create virtual environment
echo "[INFO] Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "[INFO] Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "[INFO] Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "[INFO] Installing dependencies..."
pip install -r requirements.txt

# Install development dependencies
echo "[INFO] Installing development dependencies..."
pip install -r requirements-dev.txt

# Create .env file
if [ ! -f ".env" ]; then
    echo "[INFO] Creating .env file from example..."
    cp .env.example .env
    echo ""
    echo "[WARNING] Please add your OPENAI_API_KEY to the .env file!"
    echo ""
fi

# Create necessary directories
mkdir -p tests docs

# Create initial test files
[ ! -f "tests/__init__.py" ] && echo "# Test package" > tests/__init__.py
[ ! -f "tests/test_app.py" ] && echo "# Test app" > tests/test_app.py
[ ! -f "tests/test_moderator.py" ] && echo "# Test moderator" > tests/test_moderator.py

# Create moderation log
[ ! -f "moderation_log.json" ] && echo "[]" > moderation_log.json

# Create README if it doesn't exist
[ ! -f "README.md" ] && cat > README.md << 'EOF'
# AI Comment Moderator

A REST API for AI-powered comment moderation with appeal system.

## Quick Start
1. Add your OPENAI_API_KEY to .env file
2. Run: python app.py
3. Server runs on http://localhost:5000
EOF

# Initial Git commit
if [ "$GIT_AVAILABLE" = true ] && [ -d ".git" ]; then
    echo "[INFO] Creating initial Git commit..."
    git add .
    git commit -m "Initial commit: AI Comment Moderator with Appeal System" 2>/dev/null || true
fi

echo ""
echo "========================================"
echo " Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Add your OPENAI_API_KEY to .env file"
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo "3. Run the server:"
echo "   python app.py"
echo "4. To use Git:"
echo "   git remote add origin https://github.com/yourusername/repo.git"
echo "   git push -u origin main"
echo ""