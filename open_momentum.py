"""
This code runs momentum trades on the first half hour of the market.
It uses the data prepared in v2_organize_backtest_data.py, which creates the file spy_intraday_processed.pkl
This module assumes:
All data is preparared elsewhere.
Data is passed in as a normalized in-memory object
No network, no files, no vendors, no APIs needed in this

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
- Session: Regular trading hours only, 09:30 to 16:00 ET
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
-actual trading function, record each trade, p and l not now - later
-seperate script - calculate p and l for each strategy, metrics
-the code should return labeled things that have each trade in them, insdie a daddi file, which could then be passed
to the script that calculates p and l and the metrics. 🔥
One more thing, which is obvious from the above: the code should do by strategy, and not by day, even though this will take longer for the computation. It's way simpler cleaner reusable code.

"""

##imports

def data_loading(thingie_shmegegie):
    #TODO load the data from the file spy_intraday...
    #TODO make sure it's there, at least mostly - maybe just pass to script called test.py which is already a test of this...
    #TODO put out an error for one of the first two issues, stop if issue, if not 
    #TODO return the thingie in memory assuming all is good.
    #that's it for this function. sorta did this already - tested.. but want it to be in the script
def trade_strategies ():
    #TODO make a loop with number of minute bars  of the momentum I'm caring about that defines direction  - 1, 3, 5, 10, 15, for now, but not hardcoded...
    #TODO make a variable with the holding time - for this specific code it's just whatever the momentum was, but it should
    ##be a seperate varible because it's way easier this way. I'm gonna mannualy make them the same, so that it's reusable. No
    ##this code won't be making the matrix like last time, but maybe, just maybe, it's a good idea. Ok, I have no patience - once I
    #go there it's the same confusing. haha im talking to myself haha 🤣
    #TODO should return both these loops 
def define_trades():  ##this might get nuts in the head becaues the days are all one fat thingie!! gotta make sure I'm not doing trillions of computations
    #TODO function runs on loop grandpa - through all the strategies
    # which then runs on loop dadi - goes through days on by one
    #TODO for each strategy, day in strategy
    #take the time passed from momentum - and define direction of trade #for future code - only trade if the momentum is strong - don't have a measure yet, but basicly not too deep low past open if direction long etc.
    #then define the price trade is placed at - the open of the next bar
    #then define the price of exit
    #return a set of trades based on entry, exit, direction. no need anymore for the day. pass for each strategy seperate or something - not sure yet.
def day_trader(thing_from_last_function): #this function places the trades, based on the info from the last one
    #TODO grab the data from last thingie
    #and then just do each trade, how much won or lost, list of big numbers
    #group by each strategy - more like don't mix up by each strategy, csuase it starts together
    #return groups of lists of numbers with labels by each strategy
def main():
    #TODO this stupid most annoying and hardest part lol 😂







