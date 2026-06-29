from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from moderator import AIModerator
from logger import ModerationLogger
from config import Config
import time
from collections import defaultdict
import os
import json

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize components
moderator = AIModerator()
logger = ModerationLogger()

# Rate limiting (mobile-optimized - higher limits for mobile users)
rate_limits = defaultdict(list)
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX = 15     # Higher for mobile users

# In-memory storage for mobile sessions
mobile_sessions = {}

def check_rate_limit(user_id):
    """Simple rate limiting per user"""
    if user_id is None:
        return True
    
    now = time.time()
    # Clean old entries
    rate_limits[user_id] = [t for t in rate_limits[user_id] if now - t < RATE_LIMIT_WINDOW]
    
    if len(rate_limits[user_id]) >= RATE_LIMIT_MAX:
        return False
    
    rate_limits[user_id].append(now)
    return True

# Mobile-friendly API endpoints
@app.route('/')
def index():
    return render_template('mobile/index.html')

@app.route('/moderate-page')
def moderate_page():
    return render_template('mobile/moderate.html')

@app.route('/appeal-page')
def appeal_page():
    return render_template('mobile/appeal.html')

@app.route('/api/moderate', methods=['POST'])
def moderate_comment_mobile():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request body"}), 400
        
        comment = data.get('comment', '').strip()
        user_id = data.get('user_id', 'mobile_user_' + str(int(time.time())))
        
        # Validate mobile-specific fields
        device_type = data.get('device_type', 'mobile')
        
        # Edge case: Empty comment
        if not comment:
            return jsonify({
                "success": False,
                "error": "Comment cannot be empty",
                "decision": "rejected",
                "confidence": 1.0,
                "reasoning": "Empty comment rejected"
            }), 400
        
        # Edge case: Very long comment (mobile-friendly limit)
        if len(comment) > Config.MAX_COMMENT_LENGTH:
            return jsonify({
                "success": False,
                "error": f"Comment exceeds maximum length of {Config.MAX_COMMENT_LENGTH} characters",
                "decision": "flagged_for_review",
                "confidence": 0.8,
                "reasoning": "Comment unusually long - flagged for review"
            }), 400
        
        # Rate limiting
        if not check_rate_limit(user_id):
            return jsonify({
                "success": False,
                "error": "Rate limit exceeded. Please wait 60 seconds.",
                "decision": "rejected",
                "confidence": 1.0,
                "reasoning": "Rate limit exceeded"
            }), 429
        
        # Moderate the comment
        result = moderator.moderate_comment(comment)
        
        # Log the decision
        logger.log_decision(
            comment=comment,
            decision=result['decision'],
            confidence=result['confidence'],
            reasoning=result['reasoning'],
            category=result.get('category', 'uncategorized'),
            is_appeal=False
        )
        
        # Mobile-optimized response
        return jsonify({
            "success": True,
            "decision": result['decision'],
            "confidence": result['confidence'],
            "reasoning": result['reasoning'],
            "category": result.get('category', 'uncategorized'),
            "appeal_eligible": result['decision'] == 'rejected',
            "device_type": device_type,
            "timestamp": time.time()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "decision": "flagged_for_review",
            "confidence": 0.0,
            "reasoning": f"System error: {str(e)}"
        }), 500

@app.route('/api/appeal', methods=['POST'])
def appeal_decision_mobile():
    """Mobile-optimized appeal endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request body"}), 400
        
        comment = data.get('comment', '').strip()
        appeal_context = data.get('appeal_context', '').strip()
        user_id = data.get('user_id', 'mobile_user_' + str(int(time.time())))
        
        # Validation
        if not comment:
            return jsonify({
                "success": False,
                "error": "Comment cannot be empty",
                "decision": "rejected"
            }), 400
        
        if not appeal_context:
            return jsonify({
                "success": False,
                "error": "Appeal context is required",
                "decision": "rejected",
                "confidence": 1.0,
                "reasoning": "No appeal context provided"
            }), 400
        
        if len(appeal_context) > Config.MAX_COMMENT_LENGTH:
            return jsonify({
                "success": False,
                "error": f"Appeal context exceeds maximum length of {Config.MAX_COMMENT_LENGTH} characters"
            }), 400
        
        # Rate limiting (stricter for appeals)
        if not check_rate_limit(f"{user_id}_appeal"):
            return jsonify({
                "success": False,
                "error": "Rate limit exceeded for appeals. Please wait.",
                "decision": "rejected",
                "confidence": 1.0,
                "reasoning": "Rate limit exceeded"
            }), 429
        
        # Re-evaluate with appeal context
        result = moderator.moderate_comment(comment, appeal_context)
        
        # If still rejected after appeal, no further appeals
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
        
        # Mobile-optimized response
        return jsonify({
            "success": True,
            "decision": result['decision'],
            "confidence": result['confidence'],
            "reasoning": result['reasoning'],
            "category": result.get('category', 'uncategorized'),
            "final_decision": True,
            "timestamp": time.time()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "decision": "flagged_for_review",
            "confidence": 0.0,
            "reasoning": f"System error: {str(e)}"
        }), 500

@app.route('/api/log', methods=['GET'])
def get_logs_mobile():
    """Mobile-optimized log retrieval"""
    try:
        limit = request.args.get('limit', 50, type=int)  # Lower limit for mobile
        if limit > 200:
            limit = 200
        
        logs = logger.get_logs(limit)
        
        # Mobile-optimized response (minimal data)
        mobile_logs = []
        for log in logs:
            mobile_logs.append({
                "timestamp": log['timestamp'][:10],  # Just date for mobile
                "decision": log['decision'],
                "confidence": round(log['confidence'], 2),
                "comment_preview": log['comment'][:50] + "..." if len(log['comment']) > 50 else log['comment']
            })
        
        return jsonify({
            "success": True,
            "count": len(mobile_logs),
            "logs": mobile_logs
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check_mobile():
    user_agent = request.headers.get('User-Agent', '')
    is_mobile = any(mobile in user_agent.lower() for mobile in ['mobile', 'android', 'iphone', 'ipad', 'phone'])
    
    return jsonify({
        "status": "healthy",
        "model": Config.MODEL,
        "max_comment_length": Config.MAX_COMMENT_LENGTH,
        "is_mobile": is_mobile,
        "platform": "cross-platform",
        "api_version": "1.0.0"
    })

# Serve static files
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
