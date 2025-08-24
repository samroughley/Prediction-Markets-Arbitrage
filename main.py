"""
Controls all the necessary backend functions, including:
* Calls APIs to collect data
* Performs anlysis on the data to identify arbitrage opportunites
* Saves the results of the analysis
"""

# Import necessary packages
import json

from bookie_functions import update_odds, request_odds_api, process_odds
from analysis import check_for_arbitrage
from polymarket_functions import fetch_all_markets, introduce_polymarket_odds



# Temporary booleans
update_bookie_odds = False

if update_bookie_odds:
    update_odds(save_fpath="Data/bookies_odds.json")



check_for_arbitrage(bookies_odds_fpath="Data/bookies_odds.json",
                    save_file_fpath="Data/analysed_odds.json")


    
introduce_polymarket_odds(bookies_odds_fpath="Data/bookies_odds.json",
                          updated_file_fpath="Data/bookies_odds_with_polymarket.json")

check_for_arbitrage(bookies_odds_fpath="Data/bookies_odds_with_polymarket.json",
                    save_file_fpath="Data/analysed_odds_with_polymarket.json",
                    consider_converse_outcomes=True)