#!/usr/bin/env python

import sys
import os
import importlib

def test_imports():
    required_modules = [
        'flask',
        'openai',
        'dotenv',
        'flask_cors'
    ]
    
    print("Testing imports...")
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module} - OK")
        except ImportError as e:
            print(f"❌ {module} - FAILED: {e}")
            return False
    return True

def test_env_file():
    """Check if .env file exists"""
    if os.path.exists('.env'):
        print("✅ .env file exists")
        # Check if it has the API key
        with open('.env', 'r') as f:
            content = f.read()
            if 'OPENAI_API_KEY' in content and 'your_openai_api_key_here' not in content:
                print("✅ OPENAI_API_KEY appears to be set")
                return True
            else:
                print("⚠️ OPENAI_API_KEY not set or using placeholder")
                print("   Please edit .env and add your actual API key")
                return False
    else:
        print("❌ .env file not found!")
        print("   Creating .env file from template...")
        with open('.env', 'w') as f:
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
        print("   Please edit .env and add your actual API key")
        return False

def test_directories():
    """Check required directories"""
    required_dirs = ['templates/mobile', 'static/css', 'static/js']
    all_exist = True
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path} - exists")
        else:
            print(f"⚠️ {dir_path} - missing (creating...)")
            os.makedirs(dir_path, exist_ok=True)
            all_exist = False
    
    return True

def main():
    print("="*50)
    print("AI Comment Moderator - Setup Test")
    print("="*50)
    print()
    
    # Test imports
    if not test_imports():
        print("\n❌ Please install missing packages:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Test .env
    if not test_env_file():
        print("\n⚠️ Please update .env with your OpenAI API key")
        print("   Then run this test again")
        sys.exit(1)
    
    # Test directories
    test_directories()
    
    print("\n" + "="*50)
    print("✅ All tests passed!")
    print("="*50)
    print()
    print("You can now run:")
    print("1. python app.py          (Desktop version)")
    print("2. python mobile_app.py   (Mobile version)")
    print()
    print("Access at: http://localhost:5000")

if __name__ == "__main__":
    main()