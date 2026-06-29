import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    MAX_COMMENT_LENGTH = 5000
    LOG_FILE = 'moderation_log.json'
    MODEL = 'gpt-4o-mini'  
    TEMPERATURE = 0.3