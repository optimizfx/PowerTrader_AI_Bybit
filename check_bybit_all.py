import os
import time
import json
from pybit.unified_trading import HTTP
import logging

# Disable pybit info logging
logging.getLogger("pybit").setLevel(logging.WARNING)

def check_all():
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
        
        for cat in ["spot", "linear", "inverse", "option"]:
            print(f"\n--- Checking {cat.upper()} ---")
            
            # Use a wide time range or just many results
            orders = session.get_order_history(category=cat, limit=10)
            print(f"Orders: {len(orders.get('result', {}).get('list', []))}")
            if orders.get('result', {}).get('list'):
                print(f"Sample Order Symbols: {[o['symbol'] for o in orders['result']['list']]}")
            
            execs = session.get_executions(category=cat, limit=10)
            print(f"Executions: {len(execs.get('result', {}).get('list', []))}")
            
            pos = session.get_positions(category=cat, limit=10)
            print(f"Positions: {len(pos.get('result', {}).get('list', []))}")
            if pos.get('result', {}).get('list'):
                print(f"Sample Position Symbols: {[p['symbol'] for p in pos['result']['list']]}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_all()
