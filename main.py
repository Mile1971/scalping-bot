from pybit.unified_trading import HTTP
import os

# API ključevi – zameni tvojim ako testiraš lokalno, ali na Railway ćemo ih uneti kao promenljive okruženja
api_key = os.getenv("BYBIT_API_KEY")
api_secret = os.getenv("BYBIT_API_SECRET")

# Inicijalizacija konekcije sa Bybit SPOT tržištem (možeš promeniti 'spot' u 'linear' za futures)
session = HTTP(
    testnet=True,  # Postavi na False za pravi račun
    api_key=api_key,
    api_secret=api_secret
)

# Primer funkcije za scalping kupovinu
def place_market_buy(symbol="ETHUSDT", qty="0.01"):
    try:
        response = session.place_order(
            category="spot",  # Promeni u 'linear' za futures
            symbol=symbol,
            side="Buy",
            order_type="Market",
            qty=qty,
            time_in_force="IOC"
        )
        print("Order response:", response)
    except Exception as e:
        print("Error:", e)

# Pokretanje funkcije
if __name__ == "__main__":
    place_market_buy()
