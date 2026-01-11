import os
import time
import json
from pybit.unified_trading import HTTP
import logging

# Disable pybit info logging
logging.getLogger("pybit").setLevel(logging.WARNING)

def test_orders():
    try:
        with open('b_key.txt', 'r', encoding='utf-8') as f:
            api_key = f.read().strip()
        with open('b_secret.txt', 'r', encoding='utf-8') as f:
            api_secret = f.read().strip()
            
        with open('gui_settings.json', 'r', encoding='utf-8') as f:
            settings = json.load(f)
        
        demo = settings.get("bybit_demo", False)
        print(f"Connecting to Bybit (demo={demo})...")
        
        session = HTTP(
            demo=demo,
            api_key=api_key,
            api_secret=api_secret,
        )
        
        # Test BTCUSDT
        print("Fetching BTCUSDT orders...")
        resp = session.get_order_history(category="spot", symbol="BTCUSDT", limit=10)
        print(json.dumps(resp, indent=2))
        
        # Also test ETHUSDT
        print("\nFetching ETHUSDT orders...")
        resp_eth = session.get_order_history(category="spot", symbol="ETHUSDT", limit=10)
        print(json.dumps(resp_eth, indent=2))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_orders()
