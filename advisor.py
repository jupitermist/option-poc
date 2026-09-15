import os
import json

from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic

load_dotenv()


openai_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")

if not openai_key:
    raise ValueError("OPENAI_API_KEY not set")

if not anthropic_key:
    raise ValueError("ANTHROPIC_API_KEY not set")

openai_client = OpenAI(api_key=openai_key)
anthropic_client = Anthropic(api_key=anthropic_key)


def ask_openai(client, question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=200,
        messages=[{"role": "user", "content": question}],
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content


def ask_claude(client, question):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        messages=[{"role": "user", "content": question}],
    )
    return response.content[0].text


def compare_strategies(openai_strategy, claude_strategy):
    if openai_strategy == claude_strategy:
        print("MATCH:", openai_strategy)
        return True
    else:
        print("MISMATCH:")
        print("OpenAI:", openai_strategy)
        print("Claude:", claude_strategy)
        return False


def judge_strategies(openai_strategy, claude_strategy, openai_data, claude_data):
    judge_prompt = f"""Two anonymous advisors suggested different options strategies for a complete beginner with a 200 dollar budget who wants to avoid large losses.

Advisor A suggested: {openai_strategy}. Reason: {openai_data["reason"]}
Advisor B suggested: {claude_strategy}. Reason: {claude_data["reason"]}

Judge them only on these three criteria: cost to enter, risk of large loss, and how easy it is for a beginner to understand. Do not consider which advisor said what.
Explain the key difference in simple terms for a beginner, and give one clear recommendation on which to start with and why. Keep it under 80 words."""

    judge_response = anthropic_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role": "user", "content": judge_prompt}],
    )
    print("\n--- Advisor summary ---")
    print(judge_response.content[0].text)


def main():
    question = """I am a complete beginner in US stock options trading with a budget of about 200 US dollars. I want to avoid large losses and try one simple trade first. I have not chosen a stock yet, and I do not know where to start.
The strategy must be exactly one of these five: Long Call, Long Put, Covered Call, Cash-Secured Put, Bull Call Spread.
Respond in JSON with this exact format: {"stock_type": "what kind of stock and why", "strategy": "one of the five strategies above", "reason": "why it fits a beginner, under 40 words"}
Output only the raw JSON. Do not wrap it in markdown code blocks or backticks."""

    openai_answer = ask_openai(openai_client, question)
    print("OpenAI:", openai_answer)

    claude_answer = ask_claude(anthropic_client, question)
    print("Claude", claude_answer)

    try:
        openai_data = json.loads(openai_answer)
        claude_data = json.loads(claude_answer)
    except json.JSONDecodeError:
        print("Could not parse one of the responses. Stopping.")
        return
    openai_strategy = openai_data["strategy"]
    claude_strategy = claude_data["strategy"]

    is_match = compare_strategies(openai_strategy, claude_strategy)
    if not is_match:
        judge_strategies(openai_strategy, claude_strategy, openai_data, claude_data)


if __name__ == "__main__":
    main()
