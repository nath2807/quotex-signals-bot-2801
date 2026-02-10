import os
import time
import requests
import pandas as pd
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

SYMBOL = "EURUSD"
TIMEFRAME = "1m"

def get_price():
    url = "https://api.exchangerate.host/latest?base=EUR&symbols=USD"
    r = requests.get(url).json()
    return r["rates"]["USD"]

prices = []

def generate_signal():
    global prices
    price = get_price()
    prices.append(price)

    if len(prices) > 20:
        prices.pop(0)

    if len(prices) < 20:
        return None

    series = pd.Series(prices)
    ema_fast = series.ewm(span=5).mean().iloc[-1]
    ema_slow = series.ewm(span=13).mean().iloc[-1]

    if ema_fast > ema_slow:
        return "CALL 📈"
    elif ema_fast < ema_slow:
        return "PUT 📉"
    else:
        return None

while True:
    try:
        signal = generate_signal()
        if signal:
            message = f"""
📊 QUOTEX SIGNAL

PAIR: EUR/USD (OTC)
TIMEFRAME: 1 Minute
SIGNAL: {signal}
EXPIRY: 2 Minutes

⚠️ Trade responsibly
"""
            bot.send_message(chat_id=CHAT_ID, text=message)
            time.sleep(120)
        time.sleep(60)
    except Exception as e:
        print(e)
        time.sleep(60)
