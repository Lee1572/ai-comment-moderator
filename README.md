# 🤖 AI Comment Moderator with Appeal System
---
A REST API that automatically moderates user-submitted comments using AI, with an appeal mechanism for rejected comments. Built for PropertyTribes.com forum context.
---
## 📋 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Mobile Version](#mobile-version)
- [Project Structure](#project-structure)
- [Key Decisions](#key-decisions)
- [What I Would Improve](#what-i-would-improve)
- [Assumptions](#assumptions)
- [Troubleshooting](#troubleshooting)
- [License](#license)
---
## ✨ Features

- ✅ **AI-Powered Moderation**: Uses OpenAI GPT or mock moderator for intelligent comment filtering
- ✅ **Appeal System**: Users can appeal rejected comments with additional context
- ✅ **Rate Limiting**: Prevents API abuse (10 requests per minute per user)
- ✅ **Moderation Logging**: All decisions logged with timestamps and reasoning
- ✅ **Mobile-Friendly**: Responsive web interface for mobile devices
- ✅ **Dual Moderation Modes**: Real OpenAI integration + mock moderator for testing
- ✅ **Graceful Error Handling**: Falls back to manual review on errors
- ✅ **Categorization**: Comments categorized as spam, hate speech, misinformation, etc.

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Flask 3.0** | Web framework |
| **OpenAI 0.28.0** | AI moderation (optional) |
| **Python 3.8+** | Programming language |
| **Flask-CORS** | Cross-origin resource sharing |
| **python-dotenv** | Environment variable management |

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for version control)
- OpenAI API key (optional for mock mode)

### Windows Setup

#### Option 1: Automated Setup (Recommended)
1. Clone or download the repository
2. Double-click `setup.bat`
3. Follow the on-screen instructions
4. Add your OpenAI API key to `.env` (if using real mode)
5. Double-click `run.bat` to start the server

#### Option 2: Manual Setup
   ```cmd
# Create virtual environment
   python -m venv venv

# Activate it
   venv\Scripts\activate

# Install dependencies
   pip install -r requirements.txt

# Create .env file
   copy .env.example .env

# Edit .env and add your OpenAI API key (or leave as is for mock mode)

# Run the server
   python app.py



Mac/Linux Setup

# Make scripts executable
   chmod +x setup.sh run.sh

# Run setup
   ./setup.sh

# Add your OpenAI API key to .env (if using real mode)

# Run the server
   ./run.sh


Manual Setup (Mac/Linux)

# Create virtual environment
   python3 -m venv venv

# Activate it
   source venv/bin/activate

# Install dependencies
   pip install -r requirements.txt

# Create .env file
   cp .env.example .env

# Edit .env and add your OpenAI API key

# Run the server
   python app.py


⚙️ Configuration


Environment Variables (.env)

# OpenAI API Key (not required if using mock mode)
OPENAI_API_KEY=your_openai_api_key_here

# Set to True to use mock moderator, False to use real OpenAI
USE_MOCK=True


MODERATION MODES

This project supports two moderation modes:

Mode	               Mock Mode (Default)
File	               mock_moderator.py
Description	         Keyword-based moderation for testing
API Key Required     ❌ No

Mode	               Real OpenAI Mode
File	               moderator.py
Description	         AI-powered moderation with GPT
API Key Required     ✅ Yes


TO SWITCH MODES:

1. Via environment variable (recommended):

# In .env
USE_MOCK=False  # Set to True for mock, False for real OpenAI
OPENAI_API_KEY=your_openai_api_key_here

2. Via code change in app.py:

# For mock mode (no API key needed)
from mock_moderator import AIModerator

# For real OpenAI mode
from moderator import AIModerator



API ENDPOINTS



1. Health Check

{
    "status": "healthy",
    "model": "gpt-4o-mini",
    "max_comment_length": 5000
}

2. Moderate Comment
   POST/moderate

Request:
   {
    "comment": "What are the best practices for property investment?",
    "user_id": "test_user"
}

Response:
{
    "decision": "approved|rejected|flagged_for_review",
    "confidence": 0.95,
    "reasoning": "Brief explanation of the decision",
    "category": "appropriate|spam|hate_speech|misinformation|harassment|off_topic|borderline",
    "appeal_eligible": true|false
}

3. Submit Appeal
   POST/appeal

Request:
{
    "comment": "The market is terrible right now",
    "appeal_context": "Additional context explaining why the comment should be reconsidered",
    "user_id": "test_user"
}

Response:
{
    "decision": "approved|rejected",
    "confidence": 0.85,
    "reasoning": "Explanation of final decision",
    "category": "appropriate|spam|...",
    "final_decision": true
}

4. View Moderation Logs
   GET/log?limit=100

Response:
{
    "count": 100,
    "logs": [
        {
            "timestamp": "2024-01-01T12:00:00",
            "comment": "Original comment text",
            "decision": "approved",
            "confidence": 0.95,
            "reasoning": "Explanation...",
            "category": "appropriate",
            "is_appeal": false,
            "original_comment": null
        }
    ]
}


🧪 TESTING


Testing with PowerShell
# Test health
Invoke-RestMethod -Uri http://localhost:5000/health

# Test moderation
$body = @{
    comment = "What are the best practices for property investment?"
    user_id = "test_user"
} | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:5000/moderate -Method POST -Body $body -ContentType "application/json"

# Test appeal
$body = @{
    comment = "The market is terrible right now"
    appeal_context = "I was expressing genuine concern about falling property values."
    user_id = "test_user"
} | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:5000/appeal -Method POST -Body $body -ContentType "application/json"

# View logs
Invoke-RestMethod -Uri http://localhost:5000/log

Testing with curl (CMD)

# Test health
curl http://localhost:5000/health

# Test moderation
curl -X POST http://localhost:5000/moderate -H "Content-Type: application/json" -d "{\"comment\":\"What are the best practices for property investment?\",\"user_id\":\"test\"}"

# Test appeal
curl -X POST http://localhost:5000/appeal -H "Content-Type: application/json" -d "{\"comment\":\"The market is terrible right now\",\"appeal_context\":\"I was expressing genuine concern about falling property values.\",\"user_id\":\"test\"}"

# View logs
curl http://localhost:5000/log

Automated Test Script

# Run the test script
python test_all.py

📱 Mobile Version
The mobile version is accessible at the same URL: http://localhost:5000

Mobile Features
✅ Responsive design for all screen sizes
✅ Touch-optimized buttons and inputs
✅ Dark mode support
✅ PWA ready (installable on mobile devices)
✅ Offline support (with service worker)
✅ Character counters and validation

Access on Mobile

1. Find your computer's IP address:

# Windows
ipconfig
# Mac/Linux
ifconfig

2. On your mobile phone, open browser and go to: http://YOUR_IP:5000
3. Or use the mobile app directly: python mobile_app.py


📁 Project Structure

ai-comment-moderator/
├── .env                          # Environment variables (create from .env.example)
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore file
├── .vscode/                      # VS Code configuration
│   ├── settings.json
│   ├── launch.json
│   ├── tasks.json
│   └── extensions.json
├── app.py                        # Main Flask application
├── moderator.py                  # Real OpenAI integration
├── mock_moderator.py             # Mock moderator for testing
├── logger.py                     # Logging system
├── config.py                     # Configuration settings
├── requirements.txt              # Python dependencies
├── requirements-dev.txt          # Development dependencies
├── setup.bat                     # Windows setup script
├── setup.ps1                     # Windows PowerShell setup script
├── setup.sh                      # Unix/Mac setup script
├── run.bat                       # Windows run script
├── run.sh                        # Unix/Mac run script
├── test_setup.py                 # Setup verification script
├── moderation_log.json           # Log file (created on first run)
├── templates/
│   └── mobile/
│       ├── index.html            # Mobile homepage
│       ├── moderate.html         # Moderation page
│       └── appeal.html           # Appeal page
├── tests/                                 
│   ├── __init__.py                         
│   ├── test_app.py
│   └── test_moderator.py
├── static/
│   ├── css/
│   │   └── mobile.css            # Mobile styles
│   ├── manifest.json                       
│   ├── sw.js 
│   └── js/
│       └── mobile.js             # Mobile JavaScript
└── README.md                     # This file


🔑 KEY DECISIONS


1. Dual Moderation Modes

   Decision: Implemented both real OpenAI integration and a mock moderator
   Why: Allows testing without API costs while keeping real integration ready
   Impact: Project is accessible to anyone, regardless of OpenAI credits

2. Flask Framework

   Decision: Chose Flask over Django or FastAPI
   Why: Lightweight, easy to set up, perfect for API development
   Impact: Quick development, minimal dependencies

3. File-Based Logging

   Decision: Used JSON file instead of database
   Why: No external dependencies, easy to inspect, works on any system
   Impact: Simpler setup, but less scalable for production

4. Rate Limiting

   Decision: Implemented in-memory rate limiting
   Why: Prevents abuse while keeping implementation simple
   Impact: 10 requests per minute per user

5. Mobile-First Design

   Decision: Built responsive mobile interface
   Why: Many users access forums from mobile devices
   Impact: Better user experience across all devices


💡 WHAT I WOULD IMPROVE WITH MORE TIME


1. Database Integration

   Replace file-based logging with PostgreSQL or MongoDB
   Enable search and filtering of logs
   User authentication and profiles

2. Enhanced Moderation

   More sophisticated AI prompts
   Custom rules engine for admins
   Confidence threshold configuration

3. Notifications

  Webhooks for flagged content
  Email notifications for moderation decisions
  Real-time dashboard for moderators

4. Analytics Dashboard

   Moderation statistics and trends
   User reputation scoring
   Category distribution charts

5. Advanced Features

   Batch comment moderation
   Multi-language support
   Image and link moderation
   Custom moderation workflows

6. Performance

  Caching for repeated comments
  Asynchronous processing
  Database indexing for logs

7. Security

   API key rotation
   JWT authentication
   HTTPS enforcement
   Input sanitization

🤔 ASSUMPTIONS

1. Context: The forum context is property investment (PropertyTribes.com)
2. Language: All comments are in English
3. Users: Users are identified by a user_id for rate limiting
4. Storage: Logs can be stored in a file for demonstration purposes
5. Scale: The system handles moderate traffic (rate limits apply)
6. OpenAI: Real integration uses GPT-3.5-turbo or GPT-4
7. Mock Mode: The mock moderator sufficiently demonstrates all functionality
8. Platform: Cross-platform compatibility (Windows, Mac, Linux)


🐛 TROUBLESHOOTING


Common Issues and Solutions

1. Port 5000 Already in Use:

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :5000
kill -9 <PID>

2. OpenAI Quota Exceeded

Error: You exceeded your current quota

Solution:
   1. Add credits to your OpenAi account
   2. Switch to mock by setting USE_MOCK=True

3. Module not found

ModuleNotFoundError: No module named 'flask'

Solution: Install dependencies
   pip install -r requirements.txt

4. Virtual Environment Not Activating

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

4. Connection Refused

curl: (7) Failed to connect to localhost port 5000

Solution: Make sure the server is running

   python app.py

Debug Mode

   To enable debug logging, set DEBUG=True in config.py

      class Config:
    DEBUG = True
    # ... other settings


📄 LICENSE

This project is licensed under the MIT License - see the LICENSE file for details.

MIT License

Copyright (c) 2024 Lebohang Ramatlapeng

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


🙏 ACKNOWLEDGMENTS

   Built for PropertyTribes.com forum context
   OpenAI for providing the AI API
   Flask community for the excellent framework

👤 Credits
Developer: Lebohang Ramatlapeng

   Contact	   Details
   Email	      lebohang.ramatlapeng@gmail.com
   LinkedIn	   www.linkedin.com/in/lebohang-ramatlapeng
   GitHub	   www.github.com/lee1572
   Phone	      +27 717 333 084


Created for: AI Comment Moderator with Appeal System
Time Allocated: 4 hours
Status: ✅ Complete and Functional

📞 SUPPORT

For issues or questions:

   1. Check the troubleshooting section
   2. Review the logs in moderation_log.json
   3. Ensure your .env file is properly configured
   4. Verify the server is running: python app.py 
#   U p d a t e 
 
 
