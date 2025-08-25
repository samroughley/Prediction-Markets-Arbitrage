# Prediction-Markets-Arbitrage

<div align="center">

<!-- [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://prediction-markets-arbitrage.streamlit.app) -->

<a href="https://prediction-markets-arbitrage.streamlit.app">
  <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" 
       alt="Streamlit App" 
       width="250"/>
</a>

</div>

The initial aim of this project was to analyse prediction markets for arbitrage opportunities, with the intention of comparing prices on Polymarket and Kalshi. However, upon setting up accounts, I discovered that Kalshi currently can't be accessed unless you are from the US. Therefore, I can't access the Kalshi API to get the latest prices.

Therefore, currently this project consists only of a price tracker for markets on Polymarket. I will create a Streamlit dashboard to monitor prices.

I may then extend the project to include analysing the prices for trading opportunities, where I believe the contracts are over or under-priced. Since Polymarket is also restricted in the UK - that being I can access the prices but can't place trades - no actual trading will be performed, however the performance of the strategies can still be monitored.

### To-Do:

- [x] Connect to the Polymarket API
- [ ] Create a simple dashboard that monitors (particular) markets
- [ ] Research possible trading strategies 
- [ ] Track the performance of the implemented strategies

View the example [Streamlit dashboard](https://prediction-markets-arbitrage.streamlit.app) (may take a few minutes to load). The dashboard does not contain the latest odds, since the backend is not continually updated, however illustrates the data that is available.


