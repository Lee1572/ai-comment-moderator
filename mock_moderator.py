import json
import random

class AIModerator:
    def __init__(self):
        self.model = "mock"
        
    def moderate_comment(self, comment, appeal_context=None):
        
        # Simple keyword-based moderation
        comment_lower = comment.lower()
        
        # Check for spam
        spam_keywords = ['spam', 'click here', 'deal', 'promotion', 'advert', 'www.', '.com']
        if any(keyword in comment_lower for keyword in spam_keywords):
            return {
                "decision": "rejected",
                "confidence": 0.95,
                "reasoning": "This appears to be promotional content or spam.",
                "category": "spam"
            }
        
        # Check for hate speech
        hate_keywords = ['hate', 'stupid', 'dumb', 'idiot', 'racist']
        if any(keyword in comment_lower for keyword in hate_keywords):
            return {
                "decision": "rejected",
                "confidence": 0.92,
                "reasoning": "Content contains offensive or hateful language.",
                "category": "hate_speech"
            }
        
        # Check for property-related content
        property_keywords = ['property', 'investment', 'rent', 'landlord', 'tenant', 'buy', 'sell', 'market']
        if any(keyword in comment_lower for keyword in property_keywords):
            return {
                "decision": "approved",
                "confidence": 0.88,
                "reasoning": "Comment contains relevant property-related content.",
                "category": "appropriate"
            }
        
        # If appeal context is provided, approve
        if appeal_context:
            return {
                "decision": "approved",
                "confidence": 0.75,
                "reasoning": f"Appeal context provided: {appeal_context[:50]}... Comment reconsidered and approved.",
                "category": "appropriate"
            }
        
        # Default - flag for review
        return {
            "decision": "flagged_for_review",
            "confidence": 0.5,
            "reasoning": "Content does not clearly fit approved or rejected categories. Manual review recommended.",
            "category": "borderline"
        }