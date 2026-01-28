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

import pandas as pd
import pickle #the info type for the saving data

def data_loading(file_path):
    with open (file_path, "rb") as f:
        days=pickle.load(f)
        if not(days):
            raise ValueError ("The DF is empty") #already checked for this in a seperate script, just doing it again
    return days
def trade_strategies():
    impetus=[1,3, 5, 10, 15] #impetus is the movement before the trade
    inertia=[1,3, 5, 10, 15] #inertia is the movement inside the trade - where the trader is holding it
    strategies=[]
    for i, lookback in enumerate (impetus):
        strategies.append ({
            'impetus':lookback,
            'inertia':inertia[i]
        })
    return strategies 
def define_trades(strategies, days):  
    all_trades={}
    for strategy in strategies:
        impetus=strategy['impetus'] # it's a bit redundant that this function seperates what the previous function puts together, but it makes things simpler downstream - for naming strategies - and the code is cleaner and more clear.
        inertia=strategy['inertia'] 
        strategy_name=f'{impetus} {inertia}' #even though it's the same - it didn't have to be, and this is being optimized, for the thousanth time 🤪
        all_trades[strategy_name] = []
        for datestr, day_df in days.items():                  
            lookback_open = day_df.iloc[0]['open'] #because everything that this code is dealing with starts from 9:30 - ➡️ but this is unoptimized!!
            lookback_close = day_df.iloc[impetus - 1]['close']
            entry_price=day_df.iloc[impetus]['open']

            if lookback_open - lookback_close>0:
                direction="long"
            else:
                direction="short"
            #now we have direction, and trade entry price. Next part of the function does exit and grouping
            #in more complicated exit and entry conditions, each one would be it's own function. for now, though, I'm testing simple things and this could still be optimized for future code.
            exit_time=inertia + impetus ##in this case, inertia times two, but gotta do it right for future...
            exit_price=day_df.iloc [exit_time]['open']

            all_trades[strategy_name].append ({
                'entry': entry_price, 
                'direction': direction, 
                'exit': exit_price,
            })
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
if __name__ == "__main__":
    days = data_loading("days_file.pkl")
    strategies = trade_strategies()
    all_trades = define_trades(strategies, days)
    pnl_results = day_trader(all_trades)

    with open("pnl_results.pkl", "wb") as f:
        pickle.dump(pnl_results, f)

    print("Saved to pnl_results.pkl")






