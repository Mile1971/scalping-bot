import os
import time
from pybit.unified_trading import HTTP

# Konfiguracija iz Railway promenljivih (env vars)
api_key = os.environ.get("BYBIT_API_KEY")
api_secret = os.environ.get("BYBIT_API_SECRET")
base_url = os.environ.get("BYBIT_API_URL", "https://api.bybit.com")

session = HTTP(api_key=api_key, api_secret=api_secret)

# Parametri strategije
symbol = "ETHUSDT"
leverage = 10
risk_percent = 0.01  # 1% kapitala
take_profit_ratio = 2  # R:R 2:1
max_martingale_levels = 3

def get_balance():
    balance = session.get_wallet_balance(accountType="UNIFIED")
    usdt = balance["result"]["list"][0]["coin"][0]["walletBalance"]
    return float(usdt)

def place_trade(entry_price, capital, level):
    stake = capital * (risk_percent * (2 ** level))
    qty = round((stake * leverage) / entry_price, 4)

    tp_price = round(entry_price * (1 + (take_profit_ratio * risk_percent)), 2)
    sl_price = round(entry_price * (1 - risk_percent), 2)

    print(f"🟢 Ulaz na nivou {level+1}: {qty} {symbol}, cena: {entry_price}, TP: {tp_price}, SL: {sl_price}")

    order = session.place_order(
        category="spot",
        symbol=symbol,
        side="Buy",
        orderType="Market",
        qty=qty,
        takeProfit=str(tp_price),
        stopLoss=str(sl_price),
        timeInForce="GoodTillCancel"
    )
    return order

def run_bot():
    martingale_level = 0

    while martingale_level <= max_martingale_levels:
        try:
            capital = get_balance()
            price_data = session.get_tickers(category="spot", symbol=symbol)
            current_price = float(price_data["result"]["list"][0]["lastPrice"])

            result = place_trade(current_price, capital, martingale_level)

            print(f"🛠 Naloga poslat. Čekam 5 minuta...")
            time.sleep(300)

            # Ovde bi išla evaluacija ishoda, za sada simulacija
            trade_successful = True  # simulirano

            if trade_successful:
                print("✅ Trade uspešan. Resetujem Martingale.")
                martingale_level = 0
            else:
                print("❌ Trade neuspešan. Idemo na sledeći Martingale nivo.")
                martingale_level += 1

        except Exception as e:
            print(f"Greška: {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_bot()
