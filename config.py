"""Configuration management for Quotex Signals Bot."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for the bot."""
    
    # Telegram settings
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
    
    # Signal generation settings
    SIGNAL_INTERVAL = int(os.getenv('SIGNAL_INTERVAL', 60))
    CONFIDENCE_THRESHOLD = int(os.getenv('CONFIDENCE_THRESHOLD', 70))
    
    # Trading pairs
    TRADING_PAIRS = os.getenv('TRADING_PAIRS', 'EURUSD,GBPUSD,USDJPY').split(',')
    
    # API settings
    API_KEY = os.getenv('API_KEY', '')
    API_SECRET = os.getenv('API_SECRET', '')
    
    @classmethod
    def validate(cls):
        """Validate configuration."""
        if not cls.TELEGRAM_BOT_TOKEN or not cls.TELEGRAM_CHAT_ID:
            print("Warning: Telegram credentials not set. Telegram notifications disabled.")
        return True
