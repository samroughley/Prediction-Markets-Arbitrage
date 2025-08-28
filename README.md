# ⚽ Sports Arbitrage Dashboard (Premier League + Polymarket)

<div align="center">

<a href="https://prediction-markets-arbitrage.streamlit.app">
  <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" 
       alt="Streamlit App" 
       width="200"/>
</a>

</div>

---

## 📖 Project Overview

This dashboard monitors **arbitrage opportunities** between **traditional bookmakers**, as well as **Polymarket**, for upcoming Premier League matches.  
It highlights when discrepancies in odds make it possible to lock in a profit, and visualizes these opportunities in real time.

👉 [**Live Dashboard**](https://prediction-markets-arbitrage.streamlit.app)

---

## 📸 Demo

![Dashboard Screenshot](assets/dashboard.png)

---

## ✨ Features

- ✅ Fetches odds from multiple bookmakers + Polymarket  
- ✅ Detects arbitrage opportunities across outcomes (win/lose/draw)   
- ✅ Interactive dashboard with filtering
- ✅ Auto-refresh for real-time monitoring  

---

## 🛠 Tech Stack

- **Python 3.10+**  
- **Streamlit** – frontend & dashboard  
- **Requests / Polymarket API** – live data fetching  
- **Pandas / NumPy** – data analysis and manipulation  

---

## 🚀 Getting Started

To run the application locally, clone the repository and install dependencies:

```bash
# Clone the repo
git clone https://github.com/samroughley/Prediction-Markets-Arbitrage.git
cd Prediction-Markets-Arbitrage

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app locally
streamlit run Home.py
```

---

## 🏗 Architecture & Workflow

This project consists of two main components:

1. **Data Processing Script (`main.py`)**
   - Handles all API calls to bookmakers and Polymarket.
   - Performs the data processing, including calculating arbitrage opportunities.
   - Designed to run continuously for real-time updates.
   - **Note:** To see live updates in the dashboard, this script must be running in the background.

2. **Streamlit Dashboard (`Home.py`)**
   - Visualizes the arbitrage opportunities calculated by `main.py`.
   - Can be run independently to explore static or previously saved data.
   - For live updates, ensure `main.py` is running in parallel, either locally or on a server.

**Deployment Note:** The current deployment on Streamlit Community Cloud does **not** run `main.py` continuously. Therefore, the dashboard will display the most recent processed data rather than real-time updates.

---

## 📖 Usage

*To be completed...*

---

## 🎯 Motivation

This project was created to explore the intersection of sports betting markets and prediction markets such as Polymarket. I wanted to investigate whether arbitrage opportunities exist across traditional bookmakers and decentralized markets, and to build a tool that can surface these opportunities in real time.  

On a personal level, the project was also an opportunity to practice:
- Working with multiple APIs
- Designing a real-time data pipeline
- Building an interactive dashboard with Streamlit
- Applying concepts from finance and probability to sports analytics

Ultimately, this project serves both as a learning experience and as a demonstration of my skills in data engineering, visualization, and quantitative thinking.


---

## 📌 Future Improvements (and personal TO-DO list)

- [ ] Vary update frequency of bookmakers' odds based upon time until matches
- [ ] Drop historical matches without requiring API call
- [ ] Improve efficiency by storing upcoming match information, reducing Polymarket API calls (currently ~1 minute between updates)
- [ ] Incorporate other sports / competitions
- [ ] Introduce match / competition filtering on the dashboard
- [ ] Track past arbitrage opportunities
- [ ] Automatic odds updates on the Streamlit dashboard
- [ ] Improve code readability
- [ ] Create document outlining underlying maths
- [ ] Create gif for README
- [ ] Create more detailed project overview
- [ ] Remove print statements from functions in main.py
 
---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🔗 References

- Polymarket API - https://docs.polymarket.com/quickstart/introduction/main
- Premier League Odds API - https://the-odds-api.com
- Streamlit - https://streamlit.io
