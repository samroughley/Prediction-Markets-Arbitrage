"""
Controls all the necessary backend functions, including:
* Calls APIs to collect data
* Performs anlysis on the data to identify arbitrage opportunites
* Saves the results of the analysis
"""

# Import necessary packages
import json
import time
from datetime import datetime, timedelta
from tzlocal import get_localzone

from utils.bookie_functions import update_odds, request_odds_api, process_odds
from utils.analysis import check_for_arbitrage
from utils.polymarket_functions import fetch_all_markets, introduce_polymarket_odds


# Define variables
bookmakers_update_period = timedelta(hours=3)   # Keep within rate limit

# Enter a while loop
while True:
    

    # Find when bookmakers odds last updated
    with open("Data/update_times.json","r") as f:
        update_times = json.load(f)
    bookmakers_update_time = datetime.fromisoformat(update_times["Bookmakers"])

    # Get the current time
    time_now = datetime.now().astimezone()

    
    # Update bookmakers odds if necessary
    if time_now >= bookmakers_update_time + bookmakers_update_period:

        # Get latest odds
        update_odds(save_fpath="Data/bookies_odds.json")

        # Check for arbitrage
        check_for_arbitrage(bookies_odds_fpath="Data/bookies_odds.json",
                            save_file_fpath="Data/analysed_odds.json")
        
    
    # Update Polymarket odds
    introduce_polymarket_odds(bookies_odds_fpath="Data/bookies_odds.json",
                              updated_file_fpath="Data/bookies_odds_with_polymarket.json")
    
    # Check for arbitrage
    check_for_arbitrage(bookies_odds_fpath="Data/bookies_odds_with_polymarket.json",
                        save_file_fpath="Data/analysed_odds_with_polymarket.json",
                        consider_converse_outcomes=True)
    
    time.sleep(2)





"""
# Temporary booleans
update_bookie_odds = True

if update_bookie_odds:
    update_odds(save_fpath="Data/bookies_odds.json")



check_for_arbitrage(bookies_odds_fpath="Data/bookies_odds.json",
                    save_file_fpath="Data/analysed_odds.json")



introduce_polymarket_odds(bookies_odds_fpath="Data/bookies_odds.json",
                          updated_file_fpath="Data/bookies_odds_with_polymarket.json")


check_for_arbitrage(bookies_odds_fpath="Data/bookies_odds_with_polymarket.json",
                    save_file_fpath="Data/analysed_odds_with_polymarket.json",
                    consider_converse_outcomes=True)
"""

