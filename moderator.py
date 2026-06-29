import json
import openai
from config import Config
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AIModerator:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY #for V 0.28.0
        self.model = Config.MODEL
        
    def moderate_comment(self, comment, appeal_context=None):
        """Moderate a comment with optional appeal context"""
        
        # Prepare the prompt
        prompt = self._build_prompt(comment, appeal_context)
        
        try:
            # Log the prompt for debugging
            logger.debug(f"Prompt: {prompt}")
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=Config.TEMPERATURE,
                max_tokens=500
            )
            
            # Log the response
            logger.debug(f"Response: {response}")
            
            # Parse the JSON response
            content = response.choices[0].message.content
            logger.debug(f"Content: {content}")
            
            result = json.loads(content)
            
            # Validate response structure
            return self._validate_response(result, comment)
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON Parse Error: {e}")
            # Return a default response
            return {
                "decision": "flagged_for_review",
                "confidence": 0.5,
                "reasoning": "The AI response was not in the expected format. Manual review required.",
                "category": "error"
            }
        except Exception as e:
            logger.error(f"OpenAI API Error: {e}")
            # Graceful fallback
            return {
                "decision": "flagged_for_review",
                "confidence": 0.0,
                "reasoning": f"Error during moderation: {str(e)}. Comment flagged for manual review.",
                "category": "error"
            }
    
    def _get_system_prompt(self):
        return 
    
    def _build_prompt(self, comment, appeal_context=None):
        prompt = f"Comment to moderate:\n\n{comment}\n\n"
        
        if appeal_context:
            prompt += f"\nAPPEAL CONTEXT: The user has provided additional context:\n{appeal_context}\n"
            prompt += "Please reconsider the original comment with this new context."
        else:
            prompt += "Provide a moderation decision with confidence score and reasoning."
            
        return prompt
    
    def _validate_response(self, result, comment):
        
        # Set default values
        validated = {
            "decision": "flagged_for_review",
            "confidence": 0.5,
            "reasoning": "Invalid response format",
            "category": "error"
        }
        
        # Validate decision
        valid_decisions = ["approved", "rejected", "flagged_for_review"]
        if "decision" in result and result["decision"] in valid_decisions:
            validated["decision"] = result["decision"]
        
        # Validate confidence
        if "confidence" in result:
            try:
                conf = float(result["confidence"])
                if 0 <= conf <= 1:
                    validated["confidence"] = conf
            except:
                pass
        
        # Validate reasoning
        if "reasoning" in result and len(str(result["reasoning"])) > 5:
            validated["reasoning"] = result["reasoning"]
        
        # Validate category
        valid_categories = ["spam", "hate_speech", "misinformation", "harassment", 
                           "off_topic", "borderline", "appropriate", "error"]
        if "category" in result and result["category"] in valid_categories:
            validated["category"] = result["category"]
        
        return validated