"""
This script contains all the functions used to analyse the prcoessed data
obtained from the APIs, to identify any arbitrage opportunities. It then 
saves the results of the analysis to be presented in a dashboard.
"""

# Import necessary packages
import json




def check_for_arbitrage(bookies_odds_fpath, save_file_fpath,consider_converse_outcomes=False):
    """
    Check for arbitrage within the odds providied by the bookies.

    Given the format of the odds (profit = (odds-1) * stake), find that
    arbitrage is possible when:

    1/odd_1 + 1/odd_2 + 1/odd_3 < 1

    This can be derived by considering the implied probabilities of each
    event under the assumption of fair odds. The above formula can be
    extended to events with an arbitrary number of outcomes.

    To calculate the guaranteed return, can use the formula:

    guaranteed return = total stake / sum( 1/odd )

    This can be derived by considering how the maximum guaranteed return
    comes when every outcome will return the same.

    consider_converse_outcomes refers to considering the binary scenario
    provided by the ability to bet on an outcome not happening on Polymarket.
    """

    # Load the odds
    with open(bookies_odds_fpath, "r") as f:
        bookies_odds = json.load(f)

    # Go through each match
    for i, match in enumerate(bookies_odds):

        # Extract the odds
        home_odds = match["home_team"]["best_odds"]
        away_odds = match["away_team"]["best_odds"]
        draw_odds = match["draw"]["best_odds"]

        # Check for arbitrage
        arb_check = 1/home_odds + 1/away_odds + 1/draw_odds

        # If arbitrage is possible, calculate the bet sizes and maximum guaranteed return
        if arb_check < 1:

            # Calculate the weights of the odds
            home_weight = 1/home_odds
            away_weight = 1/away_odds
            draw_weight = 1/draw_odds

            # Calculate the relative bet sizes
            home_stake = home_weight / arb_check
            away_stake = away_weight / arb_check
            draw_stake = draw_weight / arb_check

            # Calculate the guaranteed return
            guaranteed_return = 1 / arb_check - 1

            # Change into a percentage
            guaranteed_return_perc = guaranteed_return * 100

            # Store results
            arb_results_dict = {
                "possible":  True,
                "home_stake": home_stake,
                "away_stake": away_stake,
                "draw_stake": draw_stake,
                "guaranteed_return_perc": guaranteed_return_perc,
                "guaranteed_return_perc_annualised": (1+guaranteed_return_perc)**52-1
            }


        else:
            # Generate the results dict
            arb_results_dict = {"possible": False}

        # Add to the results in the list
        updated_match = match | {"arb": arb_results_dict}
        bookies_odds[i] = updated_match

    # Format the data
    formatted_results = format_data(bookies_odds)

    # Save the analysed results
    with open(save_file_fpath, "w") as f:
        json.dump(formatted_results, f, indent=4)


    if consider_converse_outcomes:
        """
        Check for arbitrage opportunities taking advantage of betting against
        a particular event on the prediction markets.
        """
        
        # Go through each match
        for i, match in enumerate(bookies_odds):

            # Consider each possible outcome
            for outcome in ["home_team","draw","away_team"]:

                # Check converse odds are provided
                if "converse_outcome_odds" not in match[outcome]:
                    continue

                # Get the odds
                yes_odds = match[outcome]["best_odds"]
                no_odds = match[outcome]["converse_outcome_odds"]

                # Check for arbitrage
                if (1/yes_odds + 1/no_odds) < 1:
                    # Arbitrage is possible

                    # Calculate the bet ratio
                    yes_bet = no_odds / (yes_odds + no_odds)
                    no_bet = yes_odds / (yes_odds + no_odds)

                    # Calculate the guaranteed return
                    A = (1/yes_odds + 1/no_odds)
                    guaranteed_return_perc = (1-A)/A * 100

                    bookies_odds[i][outcome]["2_bet_arb"] = {"Yes_bet_size": yes_bet,
                                                            "No_bet_size": no_bet,
                                                            "Percentage_return": guaranteed_return_perc} 
                else:
                    bookies_odds[i][outcome]["2_bet_arb"] = None

        
        # Format the data in a convenient manner
        bookies_odds = format_for_2_bet_arb(bookies_odds)

        # Save the data
        with open("Data/two_bet_arbitrage.json","w") as f:
            json.dump(bookies_odds, f, indent=4)
                     


def format_data(analysed_data):
    """
    Takes the data post-processing from the check_for_arbitrage() function
    and formats it for saving, for convenience when used to create the 
    dashboard.
    """

    # Initialise the correctly formatted dict
    formatted_results = {
        "Date": [],
        "Home Team": [],
        "Away Team": [],
        "Home Win": [],
        "Draw": [],
        "Away Win": [],
        "Home Stake": [],
        "Draw Stake": [],
        "Away Stake": [],
        "Return": [],
        "Annualised Return": []
    }

    # Add the results into the above dict
    for match in analysed_data:

        # Add the date
        formatted_results["Date"].append(match["commence_date"])

        # Odds information
        formatted_results["Home Team"].append(match["home_team"]["team_name"])
        formatted_results["Away Team"].append(match["away_team"]["team_name"])
        formatted_results["Home Win"].append(match["home_team"]["best_odds"])
        formatted_results["Draw"].append(match["draw"]["best_odds"])
        formatted_results["Away Win"].append(match["away_team"]["best_odds"])

        # Arbitrage information
        if match["arb"]["possible"]:
            formatted_results["Home Stake"].append(f"{match['arb']['home_stake']:.3f}")
            formatted_results["Draw Stake"].append(f"{match['arb']['draw_stake']:.3f}")
            formatted_results["Away Stake"].append(f"{match['arb']['away_stake']:.3f}")
            formatted_results["Return"].append(f"{match['arb']['guaranteed_return_perc']:.3f} %")
            formatted_results["Annualised Return"].append(f"{match['arb']['guaranteed_return_perc_annualised']:.3f} %")
        else:
            formatted_results["Home Stake"].append("-")
            formatted_results["Draw Stake"].append("-")
            formatted_results["Away Stake"].append("-")
            formatted_results["Return"].append("-")
            formatted_results["Annualised Return"].append("-")


    return formatted_results


def format_for_2_bet_arb(bookmakers_odds):
    """
    Formats the data in a convenient manner for monitoring two-bet
    arbitrage.
    """

    formatted_results = []

    for match in bookmakers_odds:

        # Get team info
        home_team = match["home_team"]["team_name"]
        away_team = match["away_team"]["team_name"]
        
        # Begin match dict
        match_dict = {"Match Name": f"{home_team} vs {away_team}"}

        # Initialise the dataframe
        results_dict = {
            "Team": [],
            "Yes Odds": [],
            "No Odds": [],
            "Yes Stake": [],
            "No Stake": [],
            "Return": []
        }

        for outcome, name in zip(["home_team","draw","away_team"],[home_team,"Draw",away_team]):

            results_dict["Team"].append(name)
            results_dict["Yes Odds"].append(match[outcome]["best_odds"])
            if "converse_outcome_odds" in match[outcome]:
                results_dict["No Odds"].append(match[outcome]["converse_outcome_odds"])

                if match[outcome]["2_bet_arb"] is not None:
                    results_dict["Yes Stake"].append(f"{match[outcome]['2_bet_arb']['Yes_bet_size']:.3f}")
                    results_dict["No Stake"].append(f"{match[outcome]['2_bet_arb']['No_bet_size']:.3f}")
                    results_dict["Return"].append(f"{match[outcome]['2_bet_arb']['Percentage_return']:.3f} %")

                else:
                    results_dict["Yes Stake"].append("-")
                    results_dict["No Stake"].append("-")
                    results_dict["Return"].append("-")

            else:
                results_dict["No Odds"].append("-")
                results_dict["Yes Stake"].append("-")
                results_dict["No Stake"].append("-")
                results_dict["Return"].append("-")

        # Add to the match dict
        match_dict["Arbitrage Table"] = results_dict

        # Append to results
        formatted_results.append(match_dict)
    
    return formatted_results



    
