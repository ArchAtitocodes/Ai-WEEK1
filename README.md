# 💹 Crypto Advisor Bot

## 📌 Overview

Crypto Advisor Bot is a Python-based project that acts as a beginner-friendly **cryptocurrency advisor chatbot**. It runs in two modes:

1. **CLI Chatbot** – Rule-based Q\&A via terminal
2. **Web App (Streamlit)** – Interactive chatbot with styled UI

The bot provides:

* Basic insights on crypto trends
* Sustainability analysis of coins
* Portfolio-friendly recommendations

---

## 📂 Project Structure

```
crypto-advisor-bot/
│── src/
│   ├── chatbot.py       # CLI chatbot
│   ├── app.py           # Streamlit app
│── data/
│   ├── crypto_db.json   # Offline dataset
│── requirements.txt     # Dependencies
│── README.md            # Documentation
```

---

## 🚀 Installation & Usage

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/crypto-advisor-bot.git
cd crypto-advisor-bot
```

### 2️⃣ Setup Environment

```bash
pip install -r requirements.txt
```

### 3️⃣ Run CLI Chatbot

```bash
python src/chatbot.py
```

### 4️⃣ Run Web App

```bash
streamlit run src/app.py
```

---

## 📊 Dataset

The offline database (`crypto_db.json`) contains mock data about major cryptocurrencies:

* **Bitcoin** – High energy, low sustainability
* **Ethereum** – Medium energy, balanced sustainability
* **Cardano** – Low energy, eco-friendly

The app can be extended with **CoinGecko API** for real-time market updates.

---

## 🖼️ Screenshots

* CLI chatbot running in terminal
* Streamlit web UI with chat window

*(screenshots can be added after first run)*

---

## 🧠 Reflection (50 words)

This project demonstrates **AI decision-making** at a beginner level by simulating rule-based responses in crypto advisory. While simple, it highlights how AI tools provide structured guidance, support sustainability analysis, and adapt to user queries. It also emphasizes the role of **human oversight** when interpreting and applying algorithmic advice.

---
