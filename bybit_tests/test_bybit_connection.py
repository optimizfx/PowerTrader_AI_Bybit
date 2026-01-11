import os
import time
import json
from pybit.unified_trading import HTTP
import logging

# Disable pybit info logging
logging.getLogger("pybit").setLevel(logging.WARNING)

def test_bybit():
    output = []
    
    def log(msg):
        print(msg)
        output.append(str(msg))

    log("--- Loading Credentials ---")
    try:
        with open('b_key.txt', 'r', encoding='utf-8') as f:
            api_key = f.read().strip()
        with open('b_secret.txt', 'r', encoding='utf-8') as f:
            api_secret = f.read().strip()
        log("Credentials loaded.")
    except Exception as e:
        log(f"Error loading credentials: {e}")
        return

    # 1. Test Wallet (Testnet)
    log("\n--- Testing Wallet (TESTNET) ---")
    try:
        session = HTTP(
            demo=True,
            api_key=api_key,
            api_secret=api_secret,
        )
        resp = session.get_wallet_balance(accountType="UNIFIED")
        log(json.dumps(resp, indent=2))
    except Exception as e:
        log(f"Wallet TESTNET failed: {e}")

    # 2. Test Wallet (MAINNET)
    log("\n--- Testing Wallet (MAINNET) ---")
    try:
        session_main = HTTP(
            demo=False,
            api_key=api_key,
            api_secret=api_secret,
        )
        resp = session_main.get_wallet_balance(accountType="UNIFIED")
        log(json.dumps(resp, indent=2))
        log("SUCCESS on Mainnet! You are using Mainnet keys but settings say Testnet.")
    except Exception as e:
        log(f"Wallet MAINNET failed: {e}")

    # Write to file
    with open("debug_output_2.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    print("Output saved to debug_output_2.txt")

if __name__ == "__main__":
    test_bybit()
