import os
import time
import json
from pybit.unified_trading import HTTP
import logging

# Disable pybit info logging
logging.getLogger("pybit").setLevel(logging.WARNING)

def test_long_history():
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
        
        # 30 days ago
        start_time = int((time.time() - 30 * 24 * 3600) * 1000)
        
        # Test BTCUSDT
        print(f"Fetching BTCUSDT orders since {start_time}...")
        resp = session.get_order_history(category="spot", symbol="BTCUSDT", startTime=start_time, limit=50)
        print(f"Orders: {len(resp.get('result', {}).get('list', []))}")
        
        # Test ETHUSDT
        print(f"Fetching ETHUSDT orders since {start_time}...")
        resp_eth = session.get_order_history(category="spot", symbol="ETHUSDT", startTime=start_time, limit=50)
        print(f"Orders: {len(resp_eth.get('result', {}).get('list', []))}")

        # If still empty, check without symbol
        print("\nFetching ANY spot orders since 30 days ago...")
        resp_any = session.get_order_history(category="spot", startTime=start_time, limit=50)
        print(f"Orders: {len(resp_any.get('result', {}).get('list', []))}")
        if resp_any.get('result', {}).get('list'):
             print(f"Found symbols: {set(o['symbol'] for o in resp_any['result']['list'])}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_long_history()
