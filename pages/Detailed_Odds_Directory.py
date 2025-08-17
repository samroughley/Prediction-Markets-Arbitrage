"""
Creates an additional page on the dashboard that shows the odds provided
by all of the bookies, highlighting the best odds available for each
outcome.
"""

# Import packages
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from streamlit_theme import st_theme
import json
import pandas as pd
import time
pd.options.display.float_format = "{:.2f}".format

# Set up the page
st.set_page_config(
    page_title="Test Dashboard",
    page_icon="✅",
    layout="wide"
)

# Refresh every 5 seconds
st_autorefresh(interval=5000, key='dashboard_refresh')

# Get whether the dashboard is viewed in dark mode
theme = st_theme()
if theme == None:
    # Use light mode version by default
    using_dark_mode = False
else:
    if theme["base"] == 'dark':
        using_dark_mode = True
    else:
        using_dark_mode = False

# Format the sidebar
with st.sidebar:
    st.markdown("""
               This page contains a detailed breakdown of all the odds provided by
               bookmakers provided by the API service. The odds are shown
               separately for each match. The best available odds for each match 
               outcome are highlighted in green.
               """)
    st.markdown("`Created by:`")
    linkedin_url = "https://www.linkedin.com/in/samroughley/"
    st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Sam Roughley`</a>', unsafe_allow_html=True)
    github_url = "https://github.com/samroughley"
    if using_dark_mode:
        st.markdown(f'<a href="{github_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/dark/github.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Sam Roughley`</a>', unsafe_allow_html=True)
    else:
        st.markdown(f'<a href="{github_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Sam Roughley`</a>', unsafe_allow_html=True)


# Load the data
# Use path relative to main streamlit dashboard
with open("Data/full_bookies_odds.json","r") as f:
    full_data = json.load(f)

# Go through each match
for match in full_data:
    
    # Get match info
    home_team = match["home_team"]
    away_team = match["away_team"]

    # Write the match title
    st.markdown(f"### {home_team} vs {away_team}")

    
    # Get information about the odds from each bookmaker
    all_odds = {
        "Bookmaker": [],
        home_team: [],
        "Draw": [],
        away_team: []
    }
    for bookmaker in match["bookmakers"]:

        all_odds["Bookmaker"].append(bookmaker["title"])

        for outcome in bookmaker["markets"][0]["outcomes"]:

            all_odds[outcome["name"]].append(outcome["price"])

    # Show a table of results

    all_odds_df = pd.DataFrame(all_odds)
    all_odds_df = all_odds_df.set_index("Bookmaker")
    all_odds_df = all_odds_df.T
    # Highlight max value in each row
    styled_df = all_odds_df.style.highlight_max(axis=1, color="lightgreen")  
    st.table(styled_df)