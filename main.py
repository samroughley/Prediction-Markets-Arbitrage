"""
Controls all the necessary backend functions, including:
* Calls APIs to collect data
* Performs anlysis on the data to identify arbitrage opportunites
* Saves the results of the analysis
"""

# Import necessary packages
import json

from bookie_functions import update_odds



# Temporary booleans
update_bookie_odds = False

if update_bookie_odds:
    update_odds()


