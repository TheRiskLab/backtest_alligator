"""
About this code:
This code takes intraday stock data from an API,  and saves it in a JSON format suitable for backtesting trading strategies.
Made not really reusable, sadly, but it's my first real fetching from API and I have no pateicne for making it reusable.
Next thing to know: The data is from stockdata.org, which has a free tier that allows for intraday minute data fetching.format that can be used for backtesting.
Functions and layout of the code:
First there are the imports and universal variables (too bad, I know, I know).
Api hardcoded, too bad, I know, I know. Don't bother me about it now.
Function to build the request parameters - what data I want; looping becuase it only takes seven days of intraday at a time.
Function to fetch a chunk of intraday data based on the parameters.
That's it. Updates about it when it's finished.
One more thing: I did it alreeady, so I'm just gonna do the rest now. Important not to run it
again, becuae my api calls are limited.
I put a hash befroe the api key so it won't run again by accident.
⚠️Important: The API, for some reason, isn't working to decide which dates to download, and, therefore, also doesn't
work to to the loop of groups of seven days. This deems a lot of this code useless and arbitraty, as even though the request sent is for certain days, 
it's not working.
I left as is for future fixing, sa well as that this test was for play purposes only.
I hope to come back and fix this in the future.
⚠️Important: The API is hardcoded. Get your own API for this, it's free for 100 pulls.
"""
import requests
from datetime import datetime, timedelta ##this is for the loop, tested and it works!!😂
import json  ###for the file type didn't test yet 😅

API_KEY =   #hardcoded.
BASE_URL = "https://api.stockdata.org/v1/data/intraday"
MAX_API_CALLS = 50##just for the testing time, when I do it for real I'll fix.

symbol = "SPY" 
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 29)#this is just for the first version, but I"ll update for the full dates.

def build_requests(symbol, start_date, end_date):   ##makes a group of request parameters that will be passed to the actual request function. 
    requests_params = []
    day = start_date

    while day <= end_date:   ##Working with an api that allows for a week of minute data at a time, so I have to break it up into chunks.
        chunk_start = day
        chunk_end = min(day + timedelta(days=6), end_date)

        requests_params.append({ #probably a lot of this could be done once, but too bad for now. It doens't currently make a difference for th eresult and the timing is tini anyway.
            "symbols": symbol,
            "interval": "minute",
            "date_from": chunk_start.strftime("%Y-%m-%d"),
            "date_to": chunk_end.strftime("%Y-%m-%d"),
            "api_token": API_KEY,
        })

        day = chunk_end + timedelta(days=1)
    return requests_params

def download_intraday_data(request_params):
    all_responses = []
    api_calls=0

    for params in request_params:
        if api_calls >= MAX_API_CALLS:
            break
        response = requests.get(BASE_URL, params=params, timeout=10)
        if response.status_code == 200:
            all_responses.append(response.json())
        else:
            print(f"Failed to fetch data: {response.status_code} - {response.text}")
        api_calls += 1
    return all_responses, api_calls
request_params = build_requests(symbol, start_date, end_date)
responses = download_intraday_data(request_params)
with open("2023_intra_day.json", "w") as f:
    json.dump(responses, f)

print("Saved raw data to 2023_intra_day.json")
print ("API calls used:", responses[1])



