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

*(Insert a screenshot or animated GIF of your dashboard here — highly recommended!)*  

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

Clone the repository and install dependencies:

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

*Something about usage...*

---

## 🎯 Motivation

*Something about motivation...*

---

## 📌 Future Improvements

*Something about future improvements*

- [x] To do
- [ ] To do
- [ ] To do

---

## 📜 License and References

*Something about license and references...* 

