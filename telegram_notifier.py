"""Telegram notification system for trading signals."""
import asyncio
from typing import Optional
from telegram import Bot
from telegram.error import TelegramError


class TelegramNotifier:
    """Send trading signals via Telegram."""
    
    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize Telegram notifier.
        
        Args:
            bot_token: Telegram bot API token
            chat_id: Telegram chat ID to send messages to
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.bot = None
        
        if bot_token and chat_id:
            self.bot = Bot(token=bot_token)
    
    async def send_message(self, message: str) -> bool:
        """
        Send a message via Telegram.
        
        Args:
            message: Message text to send
            
        Returns:
            True if message was sent successfully, False otherwise
        """
        if not self.bot:
            print("Telegram bot not configured")
            return False
        
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown'
            )
            return True
        except TelegramError as e:
            print(f"Failed to send Telegram message: {e}")
            return False
    
    def send_sync(self, message: str) -> bool:
        """
        Send a message synchronously.
        
        Args:
            message: Message text to send
            
        Returns:
            True if message was sent successfully, False otherwise
        """
        if not self.bot:
            return False
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.send_message(message))
