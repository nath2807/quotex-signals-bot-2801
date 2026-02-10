# quotex-signals-bot-2801

A Telegram bot that sends trading signals for the Quotex platform based on EMA (Exponential Moving Average) crossover strategy for EUR/USD currency pair.

## Features

- 📊 Real-time EUR/USD price monitoring
- 📈 EMA-based signal generation (Fast: 5, Slow: 13)
- 🤖 Automated Telegram notifications
- ⚡ Configurable polling intervals
- 🛡️ Error handling and recovery

## Prerequisites

- Python 3.7+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Telegram Chat ID

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nath2807/quotex-signals-bot-2801.git
cd quotex-signals-bot-2801
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export BOT_TOKEN="your-telegram-bot-token"
export CHAT_ID="your-telegram-chat-id"
```

4. Run the bot:
```bash
python bot.py
```

## Deployment

### Heroku

The bot includes a `Procfile` for easy deployment to Heroku:

1. Create a new Heroku app
2. Set the environment variables in Heroku config:
   ```bash
   heroku config:set BOT_TOKEN=your-telegram-bot-token
   heroku config:set CHAT_ID=your-telegram-chat-id
   ```
3. Deploy:
   ```bash
   git push heroku main
   ```

## How It Works

1. **Price Collection**: Fetches EUR/USD exchange rates every 60 seconds
2. **Signal Generation**: 
   - Maintains a rolling window of 20 price points
   - Calculates fast EMA (span=5) and slow EMA (span=13)
   - Generates CALL signal when fast EMA > slow EMA
   - Generates PUT signal when fast EMA < slow EMA
3. **Notification**: Sends signals to configured Telegram chat
4. **Cooldown**: Waits 120 seconds after sending a signal

## Configuration

Edit the constants in `bot.py` to customize behavior:

- `SIGNAL_COOLDOWN`: Seconds to wait after sending a signal (default: 120)
- `POLL_INTERVAL`: Seconds to wait between price checks (default: 60)

## Signal Format

```
📊 QUOTEX SIGNAL

PAIR: EUR/USD (OTC)
TIMEFRAME: 1 Minute
SIGNAL: CALL 📈 (or PUT 📉)
EXPIRY: 2 Minutes

⚠️ Trade responsibly
```

## Disclaimer

⚠️ **Trading involves risk. This bot is for educational purposes only. Always trade responsibly and never invest more than you can afford to lose.**

## License

This project is open source and available under the MIT License.