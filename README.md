# 🤖 AI Comment Moderator with Appeal System

A REST API that automatically moderates user-submitted comments using AI, with an appeal mechanism for rejected comments. Built for PropertyTribes.com forum context.

---

## Quick overview

- AI-powered moderation (real OpenAI or a mock keyword-based moderator)
- Appeal workflow for rejected comments
- Rate limiting (10 requests/minute per user)
- File-based JSON logging (easy to inspect)
- Mobile-friendly responsive UI (templates included)
- Graceful fallback to manual review on errors

---

## Table of contents

- Features
- Tech stack
- Quick start
- Configuration
- API
- Testing
- Project structure
- Key decisions & improvements
- Assumptions
- Troubleshooting
- License & credits

---

## Features

- ✅ **AI-Powered Moderation**: Uses OpenAI GPT or mock moderator for intelligent comment filtering
- ✅ **Appeal System**: Users can appeal rejected comments with additional context
- ✅ **Rate Limiting**: Prevents API abuse (10 requests per minute per user)
- ✅ **Moderation Logging**: All decisions logged with timestamps and reasoning
- ✅ **Mobile-Friendly**: Responsive web interface for mobile devices
- ✅ **Dual Moderation Modes**: Real OpenAI integration + mock moderator for testing
- ✅ **Graceful Error Handling**: Falls back to manual review on errors
- ✅ **Categorization**: Comments categorized as spam, hate speech, misinformation, etc.

---

## Tech stack

| Technology | Purpose |
|------------|---------|
| **Flask 3.0** | Web framework |
| **OpenAI 0.28.0** | AI moderation (optional) |
| **Python 3.8+** | Programming language |
| **Flask-CORS** | Cross-origin resource sharing |
| **python-dotenv** | Environment variable management |

---

## Quick start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for version control)
- OpenAI API key (optional for mock mode)

Clone and prepare:

Windows (recommended scripts included)
1. git clone https://github.com/Lee1572/ai-comment-moderator.git
2. Double-click `setup.bat` (or follow manual steps below)
3. Add OpenAI key to `.env` if using real mode
4. Double-click `run.bat` or run `python app.py`

Mac/Linux
1. chmod +x setup.sh run.sh
2. ./setup.sh
3. ./run.sh

Manual (cross-platform)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# mac/linux
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env, then
python app.py
```

The app runs by default on http://localhost:5000

---

## Configuration (.env)

- OPENAI_API_KEY=your_openai_api_key_here (optional)
- USE_MOCK=True  # Default True — set to False to use real OpenAI

Switching modes in code:
- Mock: from mock_moderator import AIModerator
- Real:  from moderator import AIModerator

---

## API (summary)

1) Health
GET /health
Response (example)
{
  "status":"healthy",
  "model":"gpt-4o-mini",
  "max_comment_length":5000
}

2) Moderate
POST /moderate
Request:
{
  "comment": "What are the best practices for property investment?",
  "user_id": "test_user"
}
Response:
{
  "decision": "approved" | "rejected" | "flagged_for_review",
  "confidence": 0.0-1.0,
  "reasoning": "Short explanation",
  "category": "appropriate|spam|hate_speech|misinformation|harassment|off_topic|borderline",
  "appeal_eligible": true|false
}

3) Appeal
POST /appeal
Request:
{
  "comment": "Original comment text",
  "appeal_context": "Extra context to support appeal",
  "user_id": "test_user"
}
Response:
{
  "decision": "approved" | "rejected",
  "confidence": 0.0-1.0,
  "reasoning": "Final decision explanation",
  "category": "...",
  "final_decision": true
}

4) Moderation Logs
GET /log?limit=100
Response:
{
  "count": 100,
  "logs": [ { "timestamp":"...", "comment":"...", "decision":"...", ... } ]
}

---

## Testing

PowerShell examples:
- Health: Invoke-RestMethod -Uri http://localhost:5000/health
- Moderate:
  $body = @{ comment="What are the best practices?"; user_id="test" } | ConvertTo-Json
  Invoke-RestMethod -Uri http://localhost:5000/moderate -Method POST -Body $body -ContentType "application/json"

curl examples:
- curl http://localhost:5000/health
- curl -X POST http://localhost:5000/moderate -H "Content-Type: application/json" -d '{"comment":"...","user_id":"test"}'

Run automated tests:
- python test_all.py

---

## Mobile

Mobile UI is served from the same app (templates/mobile). Features include responsive layout, touch-optimized inputs, dark mode, and basic service worker for offline support.

Mobile Features
✅ Responsive design for all screen sizes
✅ Touch-optimized buttons and inputs
✅ Dark mode support
✅ PWA ready (installable on mobile devices)
✅ Offline support (with service worker)
✅ Character counters and validation

To view on a phone:
1. Find the host IP (ipconfig / ifconfig)
2. Visit http://YOUR_IP:5000 from your phone browser

---

## Project structure (important files)

ai-comment-moderator/
- .env.example
- app.py                # Flask app and route wiring
- moderator.py          # OpenAI-powered moderator
- mock_moderator.py     # Keyword-based mock moderator
- logger.py             # JSON file logger
- config.py
- requirements.txt
- templates/mobile/     # UI templates (index, moderate, appeal)
- static/               # css, js, sw.js
- moderation_log.json   # created at runtime

---

## Key decisions

- Dual moderation mode (mock + real) so the project is usable without       OpenAI credits. 
  Project is accessible to anyone, regardless of OpenAI credits.
- Flask Framework.
  I chose Flask over Django or FastAPI.
  Lightweight, easy to setup, perfect for API development.
  Minimal dependencies.
- File-Based Logging
  Used JSON file instead of database
  No external dependencies, easy to inspect, works on any system.
  Simpler to setup, but less scalable for production.
- Rate Limiting
  Implemented in-memory rate limiting.
  Prevents abuse while keeping implementation simple
  10 requests per minute per user
-  Mobile-First Design
  Built responsive mobile interface
  Many users access forums from mobile devices
  Better user experience across all devices

---

## What I would improve more with time

- Database Integration
   Replace file-based logging with PostgreSQL or MongoDB
   Enable search and filtering of logs
   User authentication and profiles
- Enhanced Moderation
   More sophisticated AI prompts
   Custom rules engine for admins
   Confidence threshold configuration
- Notifications
   Webhooks for flagged content
   Email notifications for moderation decisions
   Real-time dashboard for moderators
- Analytics Dashboard
   Moderation statistics and trends
   User reputation scoring
   Category distribution charts
- Advanced Features
   Batch comment moderation
   Multi-language support
   Image and link moderation
   Custom moderation workflows
- Performance
  Caching for repeated comments
  Asynchronous processing
  Database indexing for logs
- Security
   API key rotation
   JWT authentication
   HTTPS enforcement
   Input sanitization

---

## Assumptions

1. Context: The forum context is property investment (PropertyTribes.com)
2. Language: All comments are in English
3. Users: Users are identified by a user_id for rate limiting
4. Storage: Logs can be stored in a file for demonstration purposes
5. Scale: The system handles moderate traffic (rate limits apply)
6. OpenAI: Real integration uses GPT-3.5-turbo or GPT-4
7. Mock Mode: The mock moderator sufficiently demonstrates all functionality
8. Platform: Cross-platform compatibility (Windows, Mac, Linux)

---

## Troubleshooting

- Port 5000 in use:
  Windows: netstat -ano | findstr :5000  → taskkill /PID <PID> /F
  Mac/Linux: lsof -i :5000 → kill -9 <PID>

- Missing dependencies:
  pip install -r requirements.txt

- OpenAI quota errors:
  Set USE_MOCK=True in .env or add account credits

- Server not starting:
  Ensure virtualenv active, run: python app.py

---

## License & credits

MIT License — see LICENSE file.

Author: Lebohang Ramatlapeng  
Contact: lebohang.ramatlapeng@gmail.com  
GitHub: https://github.com/lee1572
