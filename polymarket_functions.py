"""
This script contains all the functions to interact with the polymarket
API and save the calculated odds to be displayed on the Streamlit
dashboard.
"""

# Import necessary packages
from py_clob_client.client import ClobClient
from constants import POLYMARKET_API_KEY
import json
import re
import time


def fetch_all_markets():
    """
    Calls the API to gain information about all the markets on the site.

    Returns a list of all available markets for premier league games.
    """

    # Define host and chain ID
    host = "https://clob.polymarket.com"
    chain_id = 137  # Polygon Mainnet

    # Initialise the client
    client = ClobClient(
        host,
        key=POLYMARKET_API_KEY,
        chain_id=chain_id
    )

    # Initialise the variables
    markets_list = []
    next_cursor = None

    # Fecth all available markets
    while True:
        try:
            
            # Make API call
            if next_cursor is None:
                response = client.get_markets()
            else:
                response = client.get_markets(next_cursor=next_cursor)

            # Check if response is successful
            if 'data' not in response:
                print("No data found in response")
                break
        
            markets_list.extend(response['data'])
            next_cursor = response.get("next_cursor")

            # Exit loop if no next_cursor, indicating no more data to fetch
            if not next_cursor:
                break

        except Exception as e:
            # Print exception details for debugging
            #print(f"Exception occurred: {e}")
            #print(f"Exception details: {e.__class__.__name__}")
            #print(f"Error message: {e.args}")
            break


    return markets_list


def get_order_book_info(market_cond_id):
    """
    Returns info about the best bid and ask prices for the given market,
    as well as the order book volume.
    """
    
    # Set up API link
    host: str = "https://clob.polymarket.com"
    key: str = POLYMARKET_API_KEY 
    chain_id: int = 137 
    POLYMARKET_PROXY_ADDRESS: str = ''

    client = ClobClient(host,
                        key=key,
                        chain_id=chain_id,
                        signature_type=1,
                        funder=POLYMARKET_PROXY_ADDRESS)
    
    client.set_api_creds(client.create_or_derive_api_creds())

    # Get the data from the API
    try:
        resp = client.get_market(condition_id=market_cond_id)
    except:
        print("Market not found when finding order book")

    # Extract the wanted info
    market_info = {
        "Question": resp["question"],
        f"{resp['tokens'][0]['outcome']} price": resp['tokens'][0]['price'],
        f"{resp['tokens'][0]['outcome']} token ID": resp['tokens'][0]['token_id'],
        f"{resp['tokens'][1]['outcome']} price": resp['tokens'][1]['price'],
        f"{resp['tokens'][1]['outcome']} token ID": resp['tokens'][1]['token_id']
    }

    # Get the order book info
    try:
        yes_order_book = client.get_order_book(token_id=market_info["Yes token ID"])
        no_order_book = client.get_order_book(token_id=market_info["No token ID"])
        market_info = market_info | {"Order Book": True}
    except:
        # Order book doesn't exist
        print("Order book not found")
        return market_info | {"Order Book": False}

    # Add on order book info
    if len(yes_order_book.bids) == 0:
        market_info["Yes Best Bid"] = "N/A"
        market_info["Yes Best Bid Volume"] = "N/A"
    else:
        market_info["Yes Best Bid"] = yes_order_book.bids[-1].price
        market_info["Yes Best Bid Volume"] = yes_order_book.bids[-1].size
    if len(yes_order_book.asks) == 0:
        market_info["Yes Best Ask"] = "N/A"
        market_info["Yes Best Ask Volume"] = "N/A"
    else:
        market_info["Yes Best Ask"] = yes_order_book.asks[-1].price
        market_info["Yes Best Ask Volume"] = yes_order_book.asks[-1].size
    if len(no_order_book.bids) == 0:
        market_info["No Best Bid"] = "N/A"
        market_info["No Best Bid Volume"] = "N/A"
    else:
        market_info["No Best Bid"] = no_order_book.bids[-1].price
        market_info["No Best Bid Volume"] = no_order_book.bids[-1].size
    if len(no_order_book.asks) == 0:
        market_info["No Best Ask"] = "N/A"
        market_info["No Best Ask Volume"] = "N/A"
    else:
        market_info["No Best Ask"] = no_order_book.asks[-1].price
        market_info["No Best Ask Volume"] = no_order_book.asks[-1].size

    return market_info


def team_abr(team_name):
    """
    Returns the three letter abbreviation for the given team name.
    """

    # Make team name lower case
    team_name = team_name.lower()

    # Go through every possible team
    if team_name == "aston villa":
        # return "avl"
        return "ast"
    elif team_name == "brighton and hove albion":
        # return "bha"
        return "bri"
    elif team_name == "burnley":
        # return "brn"
        return "bur"
    elif team_name == "manchester city":
        # return "mci"
        return "mac"
    elif team_name == "manchester united":
        # return "mnu"
        return "mun"
    elif team_name == "nottingham forest":
        # return "nfo"
        return "not"
    elif team_name == "west ham united":
        return "wes"
        # return "whu"
    else:
        # Abbreviation is first three letters
        return "".join(list(team_name)[:3])



def introduce_polymarket_odds(bookies_odds_fpath, updated_file_fpath):
    """
    Takes in the currently saved bookmakers odds, and introduces the
    odds available on Polymarket. Saves the resulting odds in a separate
    file.
    """

    # Load the bookmakers' odds
    with open(bookies_odds_fpath, "r") as f:
        bookmakers_odds = json.load(f)

    # Get all the currently available Polymarket markets
    markets_list = fetch_all_markets()
        
    # Save it for now
    # import pickle
    # with open("testing_scripts/markets_list.pkl","wb") as f:
    #     pickle.dump(markets_list, f)
    # with open("testing_scripts/markets_list.pkl", "rb") as f:
    #     markets_list = pickle.load(f)
    #     print()
    #     print("Currently using archived markets list!!")
    #     print()

    # Initialise a record of all Polymarket odds
    polymarket_odds = []


    # Go through each match
    for i, match in enumerate(bookmakers_odds):

        # Get the team abbreviations
        home_team_abr = team_abr(match["home_team"]["team_name"])
        away_team_abr = team_abr(match["away_team"]["team_name"])

        # Get the match date
        match_date = match["commence_date"]

        # Construct the market slug
        home_win_market_slug = f"epl-{home_team_abr}-{away_team_abr}-{match_date}-{home_team_abr}" 
        draw_market_slug = f"epl-{home_team_abr}-{away_team_abr}-{match_date}-draw"
        away_win_market_slug = f"epl-{home_team_abr}-{away_team_abr}-{match_date}-{away_team_abr}"

        # Initialise dict
        polymarket_match_odds = {}

        # Go through the three markets
        for outcome, market_slug in zip(["home_team","draw","away_team"],[home_win_market_slug,draw_market_slug,away_win_market_slug]):

            # Get the market condition id
            cond_id = next((item["condition_id"] for item in markets_list if item["market_slug"]==market_slug), None)

            # Get market info
            if cond_id is not None:
                market_info = get_order_book_info(cond_id)
            else:
                print("Market not found")
                continue

            # For redundancy
            if not market_info["Order Book"]:
                continue

            # Get the equiavlent odds of the outcome
            ask_price = market_info["Yes Best Ask"]
            if ask_price == "N/A":
                continue
            eff_odd = 1 / float(ask_price)

            # Update the best odds if necessary
            if match[outcome]["best_odds"] < eff_odd:
                bookmakers_odds[i][outcome]["best_odds"] = eff_odd
                bookmakers_odds[i][outcome]["bookies_providing"] = "polymarket"
            elif match[outcome]["best_odds"] == eff_odd:
                bookmakers_odds[i][outcome]["bookies_providing"].append("polymarket")

            # Get the equivalent odds for the converse
            ask_price = market_info["No Best Ask"]
            if ask_price == "N/A":
                bookmakers_odds[i][outcome]["converse_outcome_odds"] = "N/A"
            else:
                bookmakers_odds[i][outcome]["converse_outcome_odds"] = 1 / float(ask_price)

            # Add to record of polymarket odds
            polymarket_match_odds[outcome] = {"Yes": eff_odd, "No": "-" if ask_price=="N/A" else 1/float(ask_price)}


        polymarket_odds.append(polymarket_match_odds)

    # Save the updated file
    with open(updated_file_fpath, "w") as f:
        json.dump(bookmakers_odds,f,indent=4)

    # Save the Polymarket odds
    with open("Data/full_polymarket_odds.json","w") as f:
        json.dump(polymarket_odds, f, indent=4)

    # Save the last update time
    try:
        with open("Data/update_times.json","r") as f:
            update_times = json.load(f)
    except:
        update_times = {}
    update_times["Polymarket"] = time.strftime('%H:%M:%S')
    with open("Data/update_times.json","w") as f:
        json.dump(update_times, f, indent=4)

    



           
           

    



