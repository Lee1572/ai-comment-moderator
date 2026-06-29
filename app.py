from flask import Flask, request, jsonify
from flask_cors import CORS
from moderator import AIModerator
from logger import ModerationLogger
from config import Config
import time
from collections import defaultdict


#1. Application Initialization
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize core components
moderator = AIModerator()  # Handles AI moderation logic
logger = ModerationLogger()  # Manages logging of all decisions

# 2. Rate Limiting Configuration
rate_limits = defaultdict(list)
RATE_LIMIT_WINDOW = 60  #seconds
RATE_LIMIT_MAX = 10     #Maximum requests per window

def check_rate_limit(user_id):
    if user_id is None:
        return True
    
    now = time.time()
    # Remove old entries outside the time window
    rate_limits[user_id] = [t for t in rate_limits[user_id] if now - t < RATE_LIMIT_WINDOW]
    
    if len(rate_limits[user_id]) >= RATE_LIMIT_MAX:
        return False  # Rate limit exceeded
    
    rate_limits[user_id].append(now)
    return True  # Within limits

# 3. Frontend Routes
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Comment Moderator API</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                border-radius: 20px;
                padding: 50px;
                max-width: 800px;
                width: 100%;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                animation: fadeIn 0.6s ease-out;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .header {
                text-align: center;
                margin-bottom: 40px;
            }
            
            .logo {
                font-size: 48px;
                margin-bottom: 10px;
            }
            
            h1 {
                color: #2d3748;
                font-size: 32px;
                font-weight: 700;
                margin-bottom: 8px;
            }
            
            .subtitle {
                color: #718096;
                font-size: 16px;
            }
            
            .status-banner {
                background: #f0fff4;
                border: 1px solid #c6f6d5;
                border-radius: 12px;
                padding: 16px 20px;
                margin-bottom: 30px;
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .status-dot {
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background: #48bb78;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            
            .status-text {
                color: #2d3748;
                font-weight: 500;
            }
            
            .status-detail {
                color: #718096;
                font-size: 14px;
                margin-left: auto;
            }
            
            .endpoints {
                margin: 30px 0;
            }
            
            .endpoint {
                background: #f7fafc;
                border-radius: 12px;
                padding: 16px 20px;
                margin-bottom: 12px;
                display: flex;
                align-items: center;
                gap: 16px;
                transition: transform 0.2s, box-shadow 0.2s;
                cursor: default;
            }
            
            .endpoint:hover {
                transform: translateX(4px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            }
            
            .method {
                font-weight: 700;
                font-size: 12px;
                padding: 4px 12px;
                border-radius: 6px;
                letter-spacing: 0.5px;
                min-width: 50px;
                text-align: center;
            }
            
            .method.get {
                background: #48bb78;
                color: white;
            }
            
            .method.post {
                background: #4299e1;
                color: white;
            }
            
            .endpoint-path {
                font-family: 'Courier New', monospace;
                font-weight: 600;
                color: #2d3748;
                flex: 1;
            }
            
            .endpoint-desc {
                color: #718096;
                font-size: 14px;
            }
            
            .badge {
                background: #ebf8ff;
                color: #2b6cb0;
                font-size: 11px;
                padding: 2px 10px;
                border-radius: 12px;
                font-weight: 600;
            }
            
            .example {
                background: #2d3748;
                border-radius: 12px;
                padding: 20px;
                margin: 20px 0;
                overflow-x: auto;
            }
            
            .example code {
                color: #e2e8f0;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                line-height: 1.6;
            }
            
            .example .comment {
                color: #a0aec0;
            }
            
            .example .string {
                color: #f6ad55;
            }
            
            .example .keyword {
                color: #63b3ed;
            }
            
            .footer {
                text-align: center;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #e2e8f0;
                color: #a0aec0;
                font-size: 14px;
            }
            
            .footer a {
                color: #667eea;
                text-decoration: none;
            }
            
            .footer a:hover {
                text-decoration: underline;
            }
            
            .quick-test {
                background: #fefcbf;
                border: 1px solid #f6e05e;
                border-radius: 12px;
                padding: 16px 20px;
                margin: 20px 0;
            }
            
            .quick-test strong {
                color: #744210;
            }
            
            .quick-test p {
                color: #744210;
                font-size: 14px;
                margin: 4px 0 8px;
            }
            
            .quick-test code {
                background: #2d3748;
                color: #e2e8f0;
                padding: 12px;
                border-radius: 8px;
                display: block;
                margin-top: 8px;
                font-size: 13px;
                overflow-x: auto;
                white-space: pre-wrap;
                word-break: break-all;
            }
            
            @media (max-width: 640px) {
                .container {
                    padding: 24px;
                }
                
                h1 {
                    font-size: 24px;
                }
                
                .endpoint {
                    flex-wrap: wrap;
                }
                
                .endpoint-desc {
                    width: 100%;
                    margin-left: 0;
                }
                
                .status-detail {
                    display: none;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🤖</div>
                <h1>Comment Moderator</h1>
                <p class="subtitle">AI-powered moderation for your community</p>
            </div>
            
            <div class="status-banner">
                <span class="status-dot"></span>
                <span class="status-text">API is running smoothly</span>
                <span class="status-detail">v1.0.0 • Ready</span>
            </div>
            
            <div class="endpoints">
                <div class="endpoint">
                    <span class="method post">POST</span>
                    <span class="endpoint-path">/moderate</span>
                    <span class="endpoint-desc">Analyze and moderate a comment</span>
                    <span class="badge">Active</span>
                </div>
                
                <div class="endpoint">
                    <span class="method post">POST</span>
                    <span class="endpoint-path">/appeal</span>
                    <span class="endpoint-desc">Reconsider a rejected comment</span>
                    <span class="badge">Active</span>
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <span class="endpoint-path">/log</span>
                    <span class="endpoint-desc">View moderation history</span>
                    <span class="badge">Active</span>
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <span class="endpoint-path">/health</span>
                    <span class="endpoint-desc">Check system status</span>
                    <span class="badge">Active</span>
                </div>
            </div>
            
            <div class="quick-test">
                <strong>🧪 Quick Test</strong>
                <p>Try it right now with curl:</p>
                <code>
                    <span style="color: #a0aec0;"># Moderate a comment</span>
                    curl -X POST http://localhost:5000/moderate \
                      -H "Content-Type: application/json" \
                      -d '{"comment": "What are the best practices for property investment?", "user_id": "test"}'
                </code>
            </div>
            
            <div class="footer">
                Built with ❤️ by <a href="https://www.linkedin.com/in/lebohang-ramatlapeng" target="_blank">Lebohang Ramatlapeng</a><br>
                <span style="font-size: 12px;">© 2024 • MIT License • <a href="https://github.com/lee1572" target="_blank">GitHub</a></span>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/favicon.ico')
def favicon():

    return '', 204

# 4. API Routes - Moderation
@app.route('/moderate', methods=['POST'])
def moderate_comment():
    try:
        # Parse and validate the request
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request body"}), 400
        
        comment = data.get('comment', '').strip()
        user_id = data.get('user_id', 'anonymous')
        
        # Input validation: Empty comments
        if not comment:
            return jsonify({
                "error": "Comment cannot be empty",
                "decision": "rejected",
                "confidence": 1.0,
                "reasoning": "Empty comment rejected"
            }), 400
        
        # Input validation: Very long comments
        if len(comment) > Config.MAX_COMMENT_LENGTH:
            return jsonify({
                "error": f"Comment exceeds maximum length of {Config.MAX_COMMENT_LENGTH} characters",
                "decision": "flagged_for_review",
                "confidence": 0.8,
                "reasoning": "Comment unusually long - flagged for review"
            }), 400
        
        # Rate limiting check
        if not check_rate_limit(user_id):
            return jsonify({
                "error": "Rate limit exceeded. Please wait before submitting more comments.",
                "decision": "rejected",
                "confidence": 1.0,
                "reasoning": "Rate limit exceeded"
            }), 429
        
        # Get the moderation decision from AI
        result = moderator.moderate_comment(comment)
        
        # Log the decision for audit purposes
        logger.log_decision(
            comment=comment,
            decision=result['decision'],
            confidence=result['confidence'],
            reasoning=result['reasoning'],
            category=result.get('category', 'uncategorized'),
            is_appeal=False
        )
        
        # Return the result
        return jsonify({
            "decision": result['decision'],
            "confidence": result['confidence'],
            "reasoning": result['reasoning'],
            "category": result.get('category', 'uncategorized'),
            "appeal_eligible": result['decision'] == 'rejected'
        })
        
    except Exception as e:
        # Graceful error handling - never crash, always return a valid response
        return jsonify({
            "error": "Internal server error",
            "decision": "flagged_for_review",
            "confidence": 0.0,
            "reasoning": f"System error: {str(e)}"
        }), 500

# 5. API Routes - Appeals
@app.route('/appeal', methods=['POST'])
def appeal_decision():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request body"}), 400
        
        comment = data.get('comment', '').strip()
        appeal_context = data.get('appeal_context', '').strip()
        user_id = data.get('user_id', 'anonymous')
        
        # Validate required fields
        if not comment:
            return jsonify({"error": "Comment cannot be empty"}), 400
        
        if not appeal_context:
            return jsonify({
                "error": "Appeal context is required",
                "decision": "rejected",
                "confidence": 1.0,
                "reasoning": "No appeal context provided"
            }), 400
        
        if len(appeal_context) > Config.MAX_COMMENT_LENGTH:
            return jsonify({
                "error": f"Appeal context exceeds maximum length of {Config.MAX_COMMENT_LENGTH} characters"
            }), 400
        
        # Stricter rate limiting for appeals
        if not check_rate_limit(f"{user_id}_appeal"):
            return jsonify({
                "error": "Rate limit exceeded for appeals. Please wait.",
                "decision": "rejected",
                "confidence": 1.0,
                "reasoning": "Rate limit exceeded"
            }), 429
        
        # Re-evaluate the comment with the appeal context
        result = moderator.moderate_comment(comment, appeal_context)
        
        # Final decision - no more appeals after this
        if result['decision'] == 'rejected':
            result['reasoning'] = f"After review of appeal context: {result['reasoning']} - Final decision, no further appeals allowed."
        
        # Log the appeal
        logger.log_decision(
            comment=comment,
            decision=result['decision'],
            confidence=result['confidence'],
            reasoning=result['reasoning'],
            category=result.get('category', 'uncategorized'),
            is_appeal=True,
            original_comment=comment
        )
        
        return jsonify({
            "decision": result['decision'],
            "confidence": result['confidence'],
            "reasoning": result['reasoning'],
            "category": result.get('category', 'uncategorized'),
            "final_decision": True
        })
        
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "decision": "flagged_for_review",
            "confidence": 0.0,
            "reasoning": f"System error: {str(e)}"
        }), 500

# 6. API Routes - Logs & Health
@app.route('/log', methods=['GET'])
def get_logs():
    try:
        limit = request.args.get('limit', 100, type=int)
        if limit > 500:
            limit = 500
        
        logs = logger.get_logs(limit)
        return jsonify({
            "count": len(logs),
            "logs": logs
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "model": Config.MODEL,
        "max_comment_length": Config.MAX_COMMENT_LENGTH
    })

# 7. Application Entry Point
if __name__ == '__main__':
    """
    Start the Flask development server.
    The server will be accessible at http://localhost:5000
    """
    app.run(debug=True, port=5000, host='0.0.0.0')