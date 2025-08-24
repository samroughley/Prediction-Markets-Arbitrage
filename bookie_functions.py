"""
This script contains all the functions used to interact with the API to
collect the latest odds provided by bookies, along with those used to
preprocess the odds.
"""

# Import necessary packages
import requests
import json
from constants import ODDS_API_KEY
import time



def request_odds_api():
    """
    Request the latest odds from the API.
    """

    # Define the necessary paramaters
    sport = 'soccer_epl'    # Get Premier League odds
    regions = 'uk'          # Get odds from UK bookies
    markets = 'h2h'         # Only pull h2h market info
    odds_format = 'decimal'
    date_format = 'iso'

    # Record time of API request
    try:
        with open("Data/update_times.json","r") as f:
            update_times = json.load(f)
    except:
        update_times = {}
    update_times["Bookmakers"] = time.strftime('%H:%M:%S')
    with open("Data/update_times.json","w") as f:
        json.dump(update_times, f, indent=4)

    # Request the api
    odds_response = requests.get(
        f'https://api.the-odds-api.com/v4/sports/{sport}/odds',
        params={
            'api_key': ODDS_API_KEY,
            'regions': regions,
            'markets': markets,
            'oddsFormat': odds_format,
            'dateFormat': date_format,
        }
    )

    # Check for a successful connection
    if odds_response.status_code != 200:
        print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')
        return {}, False
    else:
        odds_json = odds_response.json()

        # Check the usage quota
        print("Successfully collected odds")
        print('Remaining requests', odds_response.headers['x-requests-remaining'])
        print('Used requests', odds_response.headers['x-requests-used'])

        # Save all the odds
        with open("Data/full_bookies_odds.json","w") as f:
            json.dump(odds_json, f, indent=4)

        # Return the repsonse
        return odds_json, True


def process_odds(full_odds_json):
    """
    Process the odds to obtain the best available odds, and the bookies
    providing them.
    """

    # Initialise the full results
    full_results = []

    # Go through every match
    for match in full_odds_json:

        # Initialise the dicts
        home_team_dict = {"team_name": match["home_team"]}
        away_team_dict = {"team_name": match["away_team"]}

        # Get the odds from all the bookmakers
        bookmakers = match["bookmakers"]

        # Initialise the best odds dict
        best_odds_dict = {}

        # Go through all the bookies
        for bookie in bookmakers:

            # Go through each market (for redundancy)
            for market in bookie["markets"]:

                # Extra check
                if not market["key"] == "h2h":
                    continue

                # Go through the outcomes
                for outcome in market["outcomes"]:

                    if outcome["name"] not in best_odds_dict:
                        best_odds_dict[outcome["name"]] = {"best_odds": outcome["price"], "bookies_providing": [bookie["key"]]}
                    else:
                        if outcome["price"] > best_odds_dict[outcome["name"]]["best_odds"]:
                            best_odds_dict[outcome["name"]]["best_odds"] = outcome["price"]
                            best_odds_dict[outcome["name"]]["bookies_providing"] = [bookie["key"]]
                        elif outcome["price"] == best_odds_dict[outcome["name"]]["best_odds"]:
                            best_odds_dict[outcome["name"]]["bookies_providing"].append(bookie["key"])
        
        # Create the full dict
        home_team_dict = home_team_dict | best_odds_dict[home_team_dict["team_name"]]
        away_team_dict = away_team_dict | best_odds_dict[away_team_dict["team_name"]]
        full_dict = {"home_team": home_team_dict,
                    "away_team": away_team_dict,
                    "draw": best_odds_dict["Draw"]}
        
        # Add the date of the match
        full_dict["commence_date"] = match["commence_time"][:10]
        
        # Add to the full set of results
        full_results.append(full_dict)
    
    return full_results


def update_odds(save_fpath):
    """
    Performs all the necessary functions to obtain the processed odds.
    """

    # Request odds from API
    full_odds_json, successful_connection = request_odds_api()

    # Process the odds
    if successful_connection:
        processed_odds = process_odds(full_odds_json)

        # Save the results
        with open(save_fpath, "w") as f:
            json.dump(processed_odds, f, indent=4)
