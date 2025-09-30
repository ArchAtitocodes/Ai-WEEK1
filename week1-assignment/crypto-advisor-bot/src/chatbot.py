"""
Simple rule-based crypto advisor chatbot (CLI).
Usage: python chatbot.py
"""
import json
import os

HERE = os.path.dirname(__file__) if '__file__' in globals() else '.'
DATA_PATH = os.path.join(HERE, '..', 'data', 'crypto_db.json')

# Load fallback dataset
try:
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        crypto_db = json.load(f)
except Exception:
    # Fallback in-code dataset if file not found
    crypto_db = {
        "Bitcoin": {"price_trend": "rising", "market_cap": "high", "energy_use": "high", "sustainability_score": 0.3},
        "Ethereum": {"price_trend": "stable", "market_cap": "high", "energy_use": "medium", "sustainability_score": 0.6},
        "Cardano": {"price_trend": "rising", "market_cap": "medium", "energy_use": "low", "sustainability_score": 0.8},
    }

BOT_NAME = "CryptoBuddy"
DISCLAIMER = (
    "⚠️ Disclaimer: Cryptocurrency investments are risky. This bot provides simple, rule-based guidance for educational purposes only. Always do your own research."
)

# Decision rules

def profitability_score(coin):
    c = crypto_db[coin]
    score = 0
    if c.get('price_trend') == 'rising':
        score += 2
    elif c.get('price_trend') == 'stable':
        score += 1
    if c.get('market_cap') == 'high':
        score += 2
    elif c.get('market_cap') == 'medium':
        score += 1
    return score

def sustainability_score(coin):
    c = crypto_db[coin]
    score = 0
    energy = c.get('energy_use')
    if energy == 'low':
        score += 2
    elif energy == 'medium':
        score += 1
    score += float(c.get('sustainability_score', 0)) * 2
    return score

def recommend_for_goal(user_goal: str):
    user_goal = user_goal.lower()
    if any(k in user_goal for k in ('sustain', 'green', 'eco', 'energy')):
        top = max(crypto_db.keys(), key=lambda x: sustainability_score(x))
        return f"Invest in {top}! 🌱 It has the highest sustainability score in our dataset."
    if any(k in user_goal for k in ('trend', 'trending', 'long-term', 'growth', 'buy')):
        candidates = sorted(crypto_db.keys(), key=lambda x: (profitability_score(x), sustainability_score(x)), reverse=True)
        top = candidates[0]
        return f"{top} looks promising. Price trend: {crypto_db[top]['price_trend']}, market cap: {crypto_db[top]['market_cap']}."
    if 'most sustainable' in user_goal or 'most eco' in user_goal:
        top = max(crypto_db.keys(), key=lambda x: sustainability_score(x))
        return f"{top} is the most sustainable in our dataset (score {crypto_db[top]['sustainability_score']})."
    ranking = sorted(crypto_db.keys(), key=lambda x: profitability_score(x) + sustainability_score(x), reverse=True)
    return "Top coins (by composite score): " + ', '.join(ranking)

def chat_loop():
    print(f"Hi — I'm {BOT_NAME}! Ask me things like: \n- 'Which crypto is trending up?'\n- 'What's the most sustainable coin?'\n")
    print(DISCLAIMER)
    while True:
        try:
            user = input('\nYou: ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nGoodbye!')
            break
        if not user:
            continue
        if user.lower() in ('quit', 'exit', 'bye'):
            print('Bye — trade safe!')
            break
        response = recommend_for_goal(user)
        print(f"{BOT_NAME}: {response}")

if __name__ == '__main__':
    chat_loop()
# Simple rule-based crypto advisor chatbot (CLI).
# Usage: python chatbot.py