# Options Strategy Advisor

A second-opinion tool for beginners choosing their first US stock options trade.
Two AI models each suggest a strategy from live market data; a third, neutral model
resolves disagreements.

## Overview

Given a stock ticker, the tool fetches recent price data, asks OpenAI and Google
Gemini to each suggest one strategy, and compares them. When they disagree, Anthropic
Claude — which is not one of the two advisors — judges the suggestions on fixed
criteria. The tool only advises; trades are placed manually by the user.

## Why this exists

Asking a chatbot "what should I trade?" returns generic advice, because it doesn't
know today's price. This tool fetches live data first, so the suggestion responds to
the stock's actual recent movement — something a plain chat cannot do.

## Security & Robustness

* API keys isolated via `.env` (excluded from Git)
* Startup validation: missing API keys stop the program early
* Output validation: AI responses parsed as JSON; parse failures caught, not crashed
* Transient-failure handling: Gemini requests retry on server errors (503)

## Tech Stack

* Python
* OpenAI, Anthropic (Claude), Google Gemini APIs (multi-provider)
* yfinance (market data)
* Black-Scholes model (`bs.py`) from the original autopsy tool

## Setup

pip install -r requirements.txt


Add keys to `.env`:

OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GEMINI_API_KEY=...


## Usage

python advisor.py AAPL # one recommendation for a stock
python evaluate.py AAPL # measure how often the two advisors agree


## Disclaimer

Educational tool, not investment advice. The tool only suggests; the user places any
trade manually.