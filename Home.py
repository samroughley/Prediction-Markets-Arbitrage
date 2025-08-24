"""
Generates the Streamlit dashboard that shows the results from the
analysis that has been performed.
"""

# Import packages
import json
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from streamlit_theme import st_theme
import time
import pandas as pd



## Prelimaries ##

# Set up the dashboard
st.set_page_config(
    page_title="Homepage",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load the data
with open("Data/analysed_odds.json", "r") as f:
    loaded_data = json.load(f)
with open("Data/analysed_odds_with_polymarket.json", "r") as f:
    loaded_data_with_polymarket = json.load(f)
with open("Data/update_times.json","r") as f:
    update_times = json.load(f)

# Refresh every 5 seconds
st_autorefresh(interval=5000, key='dashboard_refresh')



## Construct the page ##

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

# Customise the sidebar
with st.sidebar:
    st.markdown("`Created by:`")
    linkedin_url = "https://www.linkedin.com/in/samroughley/"
    st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Sam Roughley`</a>', unsafe_allow_html=True)
    github_url = "https://github.com/samroughley"
    if using_dark_mode:
        st.markdown(f'<a href="{github_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/dark/github.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Sam Roughley`</a>', unsafe_allow_html=True)
    else:
        st.markdown(f'<a href="{github_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Sam Roughley`</a>', unsafe_allow_html=True)

    # Specify when the site was last updated
    st.write(f"""*Site last updated: {time.strftime('%H:%M:%S')}*    
             *Polymarket last update: {update_times['Polymarket']}*    
             *Bookmakers last update: {update_times['Bookmakers']}*""")

# Set the page title
st.title("Arbitrage Tracker")

# Add a description
st.markdown("""
            The table below contains the best odds provided by many of the
            UK's largest bookmakers for many of the upcoming Premier League
            matches. The compiled odds are analysed for arbitrage opportunities,
            with any arbitrage found included in the table. Details of the arbitrage
            opportunities include:

            - The relative bet sizes that should be placed on each outcome.
            - The guaranteed returns that can be achieved.
            """)

include_polymarket_data = st.checkbox(label="Include Polymarket data", value=False)



# Include the dataframe
if include_polymarket_data:
    st.dataframe(pd.DataFrame(loaded_data_with_polymarket), hide_index=True)
else:
    st.dataframe(pd.DataFrame(loaded_data), hide_index=True)

# Provide descriptions of the columns
with st.expander("ℹ️ Column details"):
    st.markdown("""
    - **Home Win:** Decimal odds for home team winning. 
    - **Draw:** Decimal odds for a draw. 
    - **Away Win:** Decimal odds for away team winning.
    - **Home Stake:** Fraction of stake that should be placed on home team winning for arbitrage.
    - **Draw Stake:** Fraction of stake that should be placed on a draw for arbitrage.
    - **Away Stake:** Fraction of stake that should be placed on away team winning for arbitrage.
    - **Return:** Maximum guaranteed percentage return from arbitrage.  
    - **Annualised Return:** Annualised return, assuming equal opportunities once a week, 52 weeks a year.
    """)


# Include table for two-bet arbitrage
st.markdown("### Two-Bet Arbitrage")
st.markdown("""Polymarket, along with other prediction markets, enables bets
            to be placed on an event not happening. This enables potential
            arbitrage opportunities that involve only two bets. Such
            opportunities are monitored below.""")

# Provide a disclaimer about update frequency
st.markdown("""*Note: Due to rate limits, the bookmakers' odds are not continually updated.
            As such, the odds presented may not be in agreement with the current odds
            available from each bookmaker. Additionally, the time since the last update from
            the API service provider can not be controlled.*""")