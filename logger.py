import json
import os
from datetime import datetime
from config import Config

class ModerationLogger:
    def __init__(self):
        self.log_file = Config.LOG_FILE
        self._initialize_log()
    
    def _initialize_log(self):
        """Create log file if it doesn't exist or is empty"""
        # Check if file exists
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f)
            return
        
        # Check if file is empty
        if os.path.getsize(self.log_file) == 0:
            with open(self.log_file, 'w') as f:
                json.dump([], f)
            return
        
        # Check if file contains valid JSON
        try:
            with open(self.log_file, 'r') as f:
                content = f.read().strip()
                if not content:
                    # File is empty or only whitespace
                    with open(self.log_file, 'w') as f2:
                        json.dump([], f2)
                    return
                json.loads(content)
        except json.JSONDecodeError:
            # File has invalid JSON, recreate it
            with open(self.log_file, 'w') as f:
                json.dump([], f)
    
    def log_decision(self, comment, decision, confidence, reasoning, category, 
                     is_appeal=False, original_comment=None):
        """Log a moderation decision"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "comment": comment,
            "decision": decision,
            "confidence": confidence,
            "reasoning": reasoning,
            "category": category,
            "is_appeal": is_appeal,
            "original_comment": original_comment if is_appeal else None
        }
        
        try:
            # Read existing logs
            with open(self.log_file, 'r') as f:
                content = f.read().strip()
                if not content:
                    logs = []
                else:
                    logs = json.loads(content)
            
            # Add new entry
            logs.append(log_entry)
            
            # Write back
            with open(self.log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except (json.JSONDecodeError, ValueError):
            # If file is corrupted, start fresh
            with open(self.log_file, 'w') as f:
                json.dump([log_entry], f, indent=2)
    
    def get_logs(self, limit=100):
        """Retrieve moderation logs"""
        try:
            with open(self.log_file, 'r') as f:
                content = f.read().strip()
                if not content:
                    return []
                logs = json.loads(content)
                return logs[-limit:]
        except (json.JSONDecodeError, ValueError, FileNotFoundError):
            return []