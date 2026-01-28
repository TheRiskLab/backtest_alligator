"""
About this code
This script takes a raw JSON file containing 1-minute intraday price data for SPY
(previously downloaded from stockdata.org) and organizes it into a canonical
pandas DataFrame suitable for backtesting.
The JSON file is right now a list, and the code should be written for this!!
The DataFrame:
- represents minute bars only (this is the source of truth)
- excludes extended hours data
- is indexed by timestamp
- is sorted chronologically
- allows gaps in the minute series (no continuity assumptions)
No aggregation is performed here.
Higher-timeframe bars (e.g. 15-minute) will be derived later from this minute-level
DataFrame by downstream code, so that intrabar movement remains accessible
after trade entry. 
This script both:
- returns the organized DataFrame for immediate use, and
- saves it to disk for reproducibility and reuse.
Scope is intentionally narrow and SPY-specific.

Code Layout
Imports
Functions: First eats the file and opens, reads it - it's a long read lol 😂😆
Then processes the data into a pandas DataFrame, then saves the DataFrame to disk
Finally, calls the functions and runs the code 
Get ready, get set, go! very simple code ahead!!!!🔥
"""

import pandas as pd 
import json
import pickle
from datetime import datetime, time 

def load_raw_data(file_path):
    with open(file_path, "r") as f:
        raw_data = json.load(f) 
    return raw_data

def process_intraday_data(entries):
    records = []

    for entry in entries:
        timestamp_str = entry.get("date") or entry.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        d = entry["data"]
        if d["is_extended_hours"]:
            continue

        records.append({ #for this backtest we don't need high and volume, but it could just be added by those names.
            "timestamp": timestamp,
            "open": d["open"],
            "low": d["low"],
            "close": d["close"],
        })

    df = pd.DataFrame(records)
    df.set_index("timestamp", inplace=True)
    df.sort_index(inplace=True)

    days = {
        day.strftime("%Y-%m-%d"): day_df
        for day, day_df in df.groupby(df.index.date)
    }

    return days

def save_object(obj, file_path):
    with open(file_path, "wb") as f:
        pickle.dump(obj, f)

def main():
    raw_file_path = "final_data_for_trades.json" 
    days_file_path = "days_file.pkl"

    raw_data = load_raw_data(raw_file_path)
    entries = raw_data[0][0]["data"]
    days = process_intraday_data(entries)

    save_object(days, days_file_path)

    return days

if __name__ == "__main__":
    days = main()