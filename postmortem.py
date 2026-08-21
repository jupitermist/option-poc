import os
import random
import json

from dotenv import load_dotenv
from anthropic import Anthropic
from bs import black_scholes_call
from collections import Counter

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

client = Anthropic(api_key=api_key)

prices = []
prev_price = None
prev_S = None

S = 600
K = 620
r = 0.05
sigma = 0.2

stock_prices = []
deltas = []
thetas = []
gammas = []
drivers = []


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
        stock_change = S - prev_S
        print(f"  price change from previous day: {round(price_change, 2)}")
        print(f"  underlying change from previous day: {round(stock_change, 2)}")

        day_prompt = f"""On this day, the option price changed by {round(price_change, 2)} and the underlying changed by {round(stock_change, 2)}. The delta was {round(delta, 3)}, the daily theta was {round(theta, 3)}, and the gamma was {round(gamma, 5)}.
Identify the single main driver of the price change.
main_driver must be one of: "delta", "theta", "gamma".
Respond in JSON with this exact format: {{"main_driver": "theta", "reason": "short explanation under 15 words"}}
Output only the raw JSON. Do not wrap it in markdown code blocks or backticks."""
        day_response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=100,
            messages=[{"role": "user", "content": day_prompt}],
        )
        day_data = json.loads(day_response.content[0].text)
        print(f" main driver: {day_data['main_driver']} ({day_data['reason']})")
        drivers.append(day_data["main_driver"])

    prev_price = price
    prev_S = S

print(prices)
driver_counts = Counter(drivers)
print(f"Main driver summary: {driver_counts}")


# prompt = f"This is a call option with strike {K} and volatility {sigma}. Over 5 days, the underlying moved through {stock_prices}, the option price moved through {prices}, the computed delta was {deltas}, the computed daily theta was {thetas}, and the computed gamma was {gammas}. Analyze what drove the option's price: separate the effect of the underlying's movement from time decay and use gamma to account for how delta itself change as the underlying moved. Use the provided delta, theta, and gamma values rather than estimating them. "
# response = client.messages.create(
#     model="claude-haiku-4-5-20251001",
#     max_tokens=400,
#     messages=[{"role": "user", "content": prompt}],
# )

# print(response.content[0].text)
