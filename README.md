# 🤖 AI Comment Moderator with Appeal System

A small REST API to automatically moderate user comments using AI, with an appeal mechanism for rejected comments. Built for PropertyTribes.com forum context.

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
- Troubleshooting
- License & credits

---

## Features

- Dual moderation modes: mock (keyword-based) and real OpenAI integration
- Appeal submission and review flow
- Per-user rate limiting
- Moderation logs in JSON with timestamps and reasoning
- Mobile-optimized templates and PWA-ready assets
- Simple file-based storage (no DB required for demo)

---

## Tech stack

- Python 3.8+
- Flask 3.0
- OpenAI (optional — used in real mode)
- Flask-CORS, python-dotenv

---

## Quick start

Prerequisites:
- Python 3.8+
- pip

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

- Dual moderation mode (mock + real) so the project is usable without OpenAI credits.
- File-based JSON logging for portability and easy inspection.
- In-memory rate limiting to keep the system simple for demos.

Planned improvements:
- Move logs to a database (Postgres/Mongo)
- Better prompt engineering and admin controls
- Webhooks/notifications and analytics dashboard
- Authentication and more robust security (HTTPS, JWT, API key rotation)

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
