"""
This code runs momentum trades on the first half hour of the market.
It uses the data prepared in v2_organize_backtest_data.py, which creates the file spy_intraday_processed.pkl
the specifics of the data are:   😄highlight it and make it clear 
This module assumes:
Data is passed in as a normalized in-memory object
No network, no files, no vendors, no APIs needed in this.

Strategy Test:
- This backtest evaluates one specific intraday hypothesis:
Whether there's momentum within the first 30 minutes of market open. 
It tests from the first minute to the next, and the first 5 to the next five, the first ten, and the first fifteen.
There is one loop, and that loop can be adjusted to test different minute intervals.

This code will be optimized for reusability, specificy - to see if it's a good trade after it's been up for all five first minute bars, etc... and not just on a one minute by minute bar...
The loops, and the running through the data, finding levels, and placing the trade and calculating P&L should all be made in a way that can be reused, each by themselves. And the code as a whole should also.
But this test is just doing minute by minute and five minute by five minute.

The strategy specification is as follows:
- Instrument: SPY
- Session: Regular trading hours only, 09:30 to 16:00 ET #the time is saved as EST.
- Data frequency: 1-minute OHLC bars (open, high, low, close)
- Bar size: 1-Minute bars
-The first move is a loop, between 1, 3, 5, 10, and 15 minute bars.
-for this context, we are simply trend following. 
-If the first bar is up, from open - close, we go long; opposite if it's down.
-Entry is right away, at the open of the next bar.
-Right now there's no stop-loss - we just exit at the close of the next bar. But the trade function should be made in a way that allows for stop-losses and take-profits to be added later.
-It calculates P&L, winning trades/losing trades ratio, and total return percentage. Also, average win, loss, and average trade.

Code layout:
- Imports
-Loading the data, making sure it's there
-trade definition/loops strategies
-finding the trade in a day
-actual trading function, record each trade, p and l not now - later-in a seperate script I'll calculate p and l for each strategy, metrics
-the code should return labeled things that have each trade in them, insdie a daddi file, which could then be passed
to the script that calculates p and l and the metrics. 🔥
One more thing, which is obvious from the above: the code should do by strategy, and not by day, even though this will take longer for the computation. It's way simpler cleaner reusable code.

"""
"""
What I have to do on the second run for optimizing reusability - today, feb 2, monday.
Will mark when each is done, so it's clear and easy for me to know and recognize.
Fix the loop that it's not a one off trade - this is bigtime a thing - cuase now it places one trade.
Regarding this, also make a max trades or window that it's trading in, bc otherwise it's super confusing.
Add variables for inertia, impetus, 👍 done
If loop for trade_type, momentum or reversal; 👍 done
True/False for long and short trades
Break up the defining the entry and defining the exit; then pass as a whole strategy to the trader.
Stop loss function for define trades, part of the exit strategy.
And now that I'm doing stop-loss, I also need intra-bar high and low, cause I could get stopped out lol.
Also this code is doing way too much - it's making strategies, definisng the trades and placing them. I'm gonna break this up and make it smaller.
Maybe even three - make the def - from basicly configure, but in groups, with a matrix option; 
and then define trades - which is basicly entry, exit on the day,
and then trader, which should really be a whole nother script but isn't for now. But maybe doesn't take much to be.

"""

import pandas as pd
import pickle #the info type for the saving data
import configure as C

def data_loading(file_path): #main will help out with this - what filepath is. Now it's in here, we'll change that.
    with open (file_path, "rb") as f:
        days=pickle.load(f)
        if not(days):
            raise ValueError ("The DF is empty") #already checked for this in a seperate script, just doing it again.
    return days

def trade_strategies(): #redundant or clean code? Well now, on v2 for reusable, it gotta have way more, so clean code 🤓 cause I don't wanna have to go fetching inside of def trades.
    impetus=C.time_to_trade #impetus is the movement before the trade, term borrowed from movement in physics.
    inertia=C.time_in_trade #inertia is the movement inside the trade - where the trader is holding it
    trade_type=C.trade_type 
    strategies=[]
    for i, lookback in enumerate (impetus):
        strategies.append ({ 
            'impetus':lookback,
            'inertia':inertia[i],
            'trade_type': trade_type
        })
    return strategies 

def define_trades(strategies, days):
    time_to_stop = C.time_to_stop
    over_lapping_trades = C.over_lapping_trades
    all_trades = {}
    
    for strategy in strategies:
        impetus = strategy['impetus']
        inertia = strategy['inertia'] 
        trade_type = strategy['trade_type']
        strategy_name = f'{impetus}_{inertia}_{trade_type}'
        all_trades[strategy_name] = {}
        
        for datestr, day_df in days.items():
            all_trades[strategy_name][datestr] = []
            
            total_bars = len(day_df)
            last_entry_bar = total_bars - inertia - 1
            
            if time_to_stop:
                last_entry_bar = min(last_entry_bar, time_to_stop)
            
            if over_lapping_trades:
                step = 1
            else:
                step = impetus + inertia
            
            current_bar = impetus
            
            while current_bar <= last_entry_bar:
                lookback_start = current_bar - impetus
                lookback_end = current_bar - 1
                
                lookback_open = day_df.iloc[lookback_start]['open']
                lookback_close = day_df.iloc[lookback_end]['close']
                entry_price = day_df.iloc[current_bar]['open']
                
                if trade_type == 'momentum': #good but redundant, clear so it's fine. But this should be later.
                    if lookback_close > lookback_open:
                        direction = "long"
                    else:
                        direction = "short"
                else:
                    if lookback_close > lookback_open:
                        direction = "short"
                    else:
                        direction = "long"
                
                exit_bar = current_bar + inertia
                exit_price = day_df.iloc[exit_bar]['open'] 
                #This isn't great code because it just grabs numbers, but the next function is going to need the stop-loss also.
                #So the question is how to make that the bars aren't working like this. I think that we should number bars by impetus/inertia, and then just
                #go from there - meaning bar 1-5, 5-10 etc, and then go from there - that the next function should loop from it, take levels etc. Not sure yet.
                
                all_trades[strategy_name][datestr].append({
                    'entry': entry_price, 
                    'direction': direction, 
                    'exit': exit_price,
                })
                
                current_bar += step
                
    return all_trades

def day_trader(all_trades): #this function excutes the actual trades
    results = {}
    for strategy_name, trades in all_trades.items():
        pnl_list = [] 

        for trade in trades:
            if trade['direction'] == 'long':
                profit = trade['exit'] - trade['entry']
                profit_percent= profit / trade['entry'] * 100
            else:
                profit = trade['entry'] - trade['exit']
                profit_percent= profit / trade['entry'] * 100
            
            pnl_list.append(profit_percent)
        
        results[strategy_name] = pnl_list
    
    return results
if __name__ == "__main__": #I'm gonna do this in the main.py, just gotta get to it.
    days = data_loading("days_file.pkl")
    strategies = trade_strategies()
    all_trades = define_trades(strategies, days)
    pnl_results = day_trader(all_trades)

    with open("pnl_results.pkl", "wb") as f:
        pickle.dump(pnl_results, f)

    print("Saved to pnl_results.pkl")






