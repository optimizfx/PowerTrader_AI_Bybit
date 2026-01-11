import os
import time
import json
from pybit.unified_trading import HTTP
import logging

# Disable pybit info logging
logging.getLogger("pybit").setLevel(logging.WARNING)

def test_positions():
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
        
        # Test Linear Positions (Futures)
        print("Fetching Linear (Futures) positions...")
        resp = session.get_positions(category="linear", settleCoin="USDT")
        print(json.dumps(resp, indent=2))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_positions()
