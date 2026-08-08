import os
from dotenv import load_dotenv
from anthropic import Anthropic
from bs import black_scholes_call



load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

client = Anthropic(api_key=api_key)

prices = []

S = 600
K = 620
r = 0.05
sigma = 0.2

import random 
stock_prices = []

for days_left in range(5, 0, -1):
    change = random.uniform(-5,5)
    S = S + change
    stock_prices.append(round(S, 2))
    T = days_left /250
    price = black_scholes_call(S=S, K=K, r=r, T=T, sigma=sigma)
    prices.append(round(float(price), 2))
    print(f"残り{days_left}日 株価={round(S,2)} 価格={round(float(price),2)}")
    
    
print(prices)

prompt = f"株価{S}、行使価格{K}、ボラティリティ{sigma}のコールオプション。価格が5日間で{prices}と推移した。何が効いてこう動いたか検死コメントして。"
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=400,
    messages=[{"role": "user", "content": prompt}])

print(response.content[0].text)