
import os
import sys

# Mock settings/paths
base_dir = os.path.dirname(os.path.abspath(__file__))
training_dir = os.path.join(base_dir, "training_data", "BTC")

print(f"Checking {training_dir}...")

tf = "1hour"

def read_file(name):
    path = os.path.join(training_dir, name)
    if not os.path.exists(path):
        print(f"MISSING: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

# 1. Read Threshold
thresh_raw = read_file(f"neural_perfect_threshold_{tf}.txt")
perfect_threshold = float(thresh_raw) if thresh_raw else 0.0
print(f"Threshold for {tf}: {perfect_threshold}")

# 2. Read Memories
mem_raw = read_file(f"memories_{tf}.txt")
memory_list = mem_raw.replace("'", "").replace(',', '').replace('"', '').replace(']', '').replace('[', '').split('~')
print(f"Loaded {len(memory_list)} memories.")

# 3. Simulate "Current Candle" (use a value from the memory file to Guarantee a match)
if len(memory_list) > 0:
    first_mem = memory_list[0].split('{}')[0].replace("'", "").replace(',', '').replace('"', '').replace(']', '').replace('[', '').split(' ')
    # The last value in memory pattern is usually the "percent change" of that candle
    # In pt_thinker, current_candle = 100 * ((close - open) / open)
    # The memory pattern seems to store these percent changes.
    
    # Let's try to match the FIRST memory exactly.
    mock_current_candle = float(first_mem[0]) 
    print(f"Mocking current candle value: {mock_current_candle}")
    
    # Run the comparison logic from pt_thinker
    mem_ind = 0
    any_perfect = 'no'
    
    memory_pattern = memory_list[mem_ind].split('{}')[0].replace("'", "").replace(',', '').replace('"', '').replace(']', '').replace('[', '').split(' ')
    memory_candle = float(memory_pattern[0]) # Start with first candle of pattern?
    
    # Wait, pt_thinker loop line 610:
    # check_dex = 0
    # memory_candle = float(memory_pattern[check_dex])
    # difference = abs((abs(current_candle - memory_candle) / ((current_candle + memory_candle) / 2)) * 100)
    
    # Let's calculate difference for the first item
    if mock_current_candle + memory_candle == 0:
        difference = 0.0
    else:
         difference = abs((abs(mock_current_candle - memory_candle) / ((mock_current_candle + memory_candle) / 2)) * 100)
         
    print(f"Difference for Memory 0: {difference} (Threshold: {perfect_threshold})")
    
    if difference <= perfect_threshold:
        print("MATCH FOUND! Logic works.")
    else:
        print("NO MATCH! Logic inconsistency.")

else:
    print("No memories to test.")
