import os
import json

from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")

openai_client = OpenAI(api_key=openai_key)
anthropic_client = Anthropic(api_key=anthropic_key)

question = """I am a complete beginner in US stock options trading with a budget of about 200 US dollars. I want to avoid large losses and try one simple trade first. I have not chosen a stock yet, and I do not know where to start.
Suggest a concrete starting point: what kind of US stock to choose (characteristics, not a specific ticker), and one beginner-friendly strategy that fits.
Respond in JSON with this exact format: {"stock_type": "what kind of stock and why", "strategy": "strategy name", "reason": "why it fits a beginner, under 40 words"}
Output only the raw JSON. Do not wrap it in markdown code blocks or backticks."""


def ask_openai(client, question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=500,
        messages=[{"role": "user", "content": question}],
    )
    return response.choices[0].message.content




def ask_claude(client, question):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": question}],
    )
    return response.content[0].text




def parse_advisor_response(answer):
    return json.loads(answer)




def compare_strategies(openai_strategy, claude_strategy):
    if openai_strategy == claude_strategy:
        print("MATCH:", openai_strategy)
    else:
        print("MISMATCH:")
        print("OpenAI:", openai_strategy)
        print("Claude:", claude_strategy)


def judge_strategies(openai_strategy, claude_strategy, openai_data, claude_data):
    judge_prompt = f"""Two AI advisors suggested different options strategies for a complete beginner with a 200 dollar budget who wants to avoid large losses.

Advisor 1 (OpenAI) suggested: {openai_strategy}. Reason: {openai_data["reason"]}
Advisor 2 (Claude) suggested: {claude_strategy}. Reason: {claude_data["reason"]}

Explain the key difference between these two strategies in simple terms for a beginner, and give one clear recommendation on which to start with and why. Keep it under 80 words."""

    judge_response = anthropic_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role": "user", "content": judge_prompt}],
    )
    print("\n--- Advisor summary ---")
    print(judge_response.content[0].text)
    
    
    
openai_answer = ask_openai(openai_client, question)
print("OpenAI:", openai_answer)

claude_answer = ask_claude(anthropic_client, question)
print("Claude", claude_answer)


openai_data = parse_advisor_response(openai_answer)
claude_data = parse_advisor_response(claude_answer)
openai_strategy = openai_data["strategy"]
claude_strategy = claude_data["strategy"]


compare_strategies(openai_strategy, claude_strategy)
judge_strategies(openai_strategy, claude_strategy, openai_data, claude_data)
