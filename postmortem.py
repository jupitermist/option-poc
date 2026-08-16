import os
import random

from dotenv import load_dotenv
from anthropic import Anthropic
from bs import black_scholes_call

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

client = Anthropic(api_key=api_key)

prices = []
prev_price = None

S = 600
K = 620
r = 0.05
sigma = 0.2

stock_prices = []
deltas = []
thetas = []
gammas = []

for days_left in range(5, 0, -1):
    change = random.uniform(-5, 5)
    S = S + change
    stock_prices.append(round(S, 2))
    T = days_left / 250
    price, delta, theta, gamma = black_scholes_call(S=S, K=K, r=r, T=T, sigma=sigma)
    prices.append(round(float(price), 2))
    deltas.append(round(delta, 3))
    thetas.append(round(theta, 3))
    gammas.append(round(gamma, 5))

    print(
        f"Day {days_left}: underlying={round(S, 2)} option={round(float(price), 2)} delta={round(delta, 3)} theta={round(theta, 3)} gamma={round(gamma, 5)}"
    )

    if prev_price is not None:
        price_change = price - prev_price
        print(f"  price change from previous day: {round(price_change, 2)}")

    prev_price = price

print(prices)


prompt = f"This is a call option with strike {K} and volatility {sigma}. Over 5 days, the underlying moved through {stock_prices}, the option price moved through {prices}, the computed delta was {deltas}, the computed daily theta was {thetas}, and the computed gamma was {gammas}. Analyze what drove the option's price: separate the effect of the underlying's movement from time decay and use gamma to account for how delta itself change as the underlying moved. Use the provided delta, theta, and gamma values rather than estimating them."
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=400,
    messages=[{"role": "user", "content": prompt}],
)

print(response.content[0].text)
