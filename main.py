import time
import requests
import hmac
import hashlib
import json
import os
from datetime import datetime

API_KEY = os.environ.get("BYBIT_API_KEY")
API_SECRET = os.environ.get("BYBIT_API_SECRET")
BASE_URL = os.environ.get("BYBIT_API_URL")

SYMBOL = "ETHUSDT"
RISK_REWARD_RATIO = 2  # 2:1
TARGET_WIN_RATE = 0.70
MAX_TRADES_PER_DAY = 60
MAX_MARTINGALE_LEVEL = 3
TARGET_DAILY_PROFIT = 0.05  # 5%

trade_count = 0
martingale_level = 0
capital = 100000  # demo kapital u USDT
profit_today = 0


def get_signature(params):
    sorted_params = sorted(params.items())
    query_string = "&".join([f"{k}={v}" for k, v in sorted_params])
    return hmac.new(bytes(API_SECRET, "utf-8"), bytes(query_string, "utf-8"), hashlib.sha256).hexdigest()


def place_order(side, qty):
    endpoint = "/v5/order/create"
    url = BASE_URL + endpoint

    params = {
        "category": "linear",
        "symbol": SYMBOL,
        "side": side,
        "orderType": "Market",
        "qty": qty,
        "timeInForce": "IOC",
        "timestamp": int(time.time() * 1000),
        "apiKey": API_KEY
    }
    params["sign"] = get_signature(params)

    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(params))
    return response.json()


def simulate_signal():
    """Simulira signal na osnovu win rate logike."""
    from random import random
    return random() < TARGET_WIN_RATE


def execute_trade():
    global trade_count, martingale_level, capital, profit_today

    if trade_count >= MAX_TRADES_PER_DAY:
        print("Max trades reached.")
        return

    stake = (capital * 0.01) * (2 ** martingale_level)
    qty = round(stake / 3400, 3)  # approx ETH price (adjustable)
    side = "Buy"

    print(f"Trade {trade_count+1}: {side} {qty} ETH @ martingale level {martingale_level}")
    result = place_order(side, qty)
    print("Order result:", result)

    win = simulate_signal()
    pnl = stake * RISK_REWARD_RATIO if win else -stake
    capital += pnl
    profit_today += pnl / 100000

    print(f"Trade result: {'WIN' if win else 'LOSS'} | PnL: {pnl:.2f} | Capital: {capital:.2f} | Daily Profit: {profit_today*100:.2f}%")

    if win:
        martingale_level = 0
    else:
        martingale_level = min(martingale_level + 1, MAX_MARTINGALE_LEVEL)

    trade_count += 1


# === Glavna petlja ===
while profit_today < TARGET_DAILY_PROFIT and trade_count < MAX_TRADES_PER_DAY:
    execute_trade()
    time.sleep(10)  # Pauza između trejdova

