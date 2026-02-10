"""Main Quotex Signals Bot implementation."""
import time
import logging
from datetime import datetime
from typing import List

from config import Config
from signal_generator import SignalGenerator
from telegram_notifier import TelegramNotifier


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class QuotexSignalsBot:
    """Main bot class for generating and sending Quotex trading signals."""
    
    def __init__(self):
        """Initialize the bot with configuration."""
        Config.validate()
        
        self.signal_generator = SignalGenerator(
            confidence_threshold=Config.CONFIDENCE_THRESHOLD
        )
        
        self.telegram_notifier = None
        if Config.TELEGRAM_BOT_TOKEN and Config.TELEGRAM_CHAT_ID:
            self.telegram_notifier = TelegramNotifier(
                bot_token=Config.TELEGRAM_BOT_TOKEN,
                chat_id=Config.TELEGRAM_CHAT_ID
            )
        
        self.trading_pairs = Config.TRADING_PAIRS
        self.signal_interval = Config.SIGNAL_INTERVAL
        
        logger.info(f"Bot initialized with {len(self.trading_pairs)} trading pairs")
        logger.info(f"Signal interval: {self.signal_interval} seconds")
    
    def send_signal(self, signal: dict) -> None:
        """
        Send a signal via available channels.
        
        Args:
            signal: Signal dictionary to send
        """
        formatted_message = self.signal_generator.format_signal_message(signal)
        
        # Log to console
        logger.info(f"Signal generated: {signal['pair']} - {signal['type']}")
        print("\n" + "="*50)
        print(formatted_message)
        print("="*50 + "\n")
        
        # Send via Telegram if configured
        if self.telegram_notifier:
            try:
                success = self.telegram_notifier.send_sync(formatted_message)
                if success:
                    logger.info("Signal sent via Telegram")
                else:
                    logger.warning("Failed to send signal via Telegram")
            except Exception as e:
                logger.error(f"Error sending Telegram notification: {e}")
    
    def run_once(self) -> None:
        """Run one iteration of signal generation."""
        logger.info("Analyzing trading pairs...")
        signals = self.signal_generator.analyze_multiple_pairs(self.trading_pairs)
        
        if signals:
            logger.info(f"Generated {len(signals)} signal(s)")
            for signal in signals:
                self.send_signal(signal)
        else:
            logger.info("No signals generated in this iteration")
    
    def run(self) -> None:
        """Run the bot continuously."""
        logger.info("Starting Quotex Signals Bot...")
        logger.info(f"Monitoring pairs: {', '.join(self.trading_pairs)}")
        
        try:
            while True:
                self.run_once()
                logger.info(f"Waiting {self.signal_interval} seconds until next analysis...")
                time.sleep(self.signal_interval)
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            raise


def main():
    """Main entry point for the bot."""
    print("""
    ╔═══════════════════════════════════════╗
    ║   QUOTEX SIGNALS BOT                  ║
    ║   Trading Signal Generator            ║
    ╚═══════════════════════════════════════╝
    """)
    
    bot = QuotexSignalsBot()
    bot.run()


if __name__ == '__main__':
    main()
