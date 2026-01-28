This folder is for backtesting a simple intraday trading strategy.
It's for experimentaion and practice, not intended for actual trading analysis.
Structure:
download_data.py
Downloads the data from an API, from stockdata.org. 
Returns a json file, unorganized and not indexed by days.
organize_data.py
Converts the json file into a dataframe, organized by days.
It returns a dataframe indexed by each day, making it easy to sort and run through
trading_engine.py
The exact strategy is defined in there, and the trades are placed.
Returns a dataframe of the percentage gains for each trade in each strategy.
calculations.py 
Takes the data from trading_engine and P&L and other numbers for the trades placed.
It prints into the terminal for a quick overveiw, and also saves to a CSV for future analysis.