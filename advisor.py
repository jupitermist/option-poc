import os
import json
import logging

from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
from google import genai

load_dotenv()
logging.getLogger("google_genai").setLevel(logging.ERROR)


openai_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

if not openai_key:
    raise ValueError("OPENAI_API_KEY not set")

if not anthropic_key:
    raise ValueError("ANTHROPIC_API_KEY not set")

if not gemini_key:
    raise ValueError("GEMINI_API_KEY not set")

openai_client = OpenAI(api_key=openai_key)
anthropic_client = Anthropic(api_key=anthropic_key)
gemini_client = genai.Client(api_key=gemini_key)


def ask_openai(client, question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=200,
        messages=[{"role": "user", "content": question}],
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content


def ask_gemini(client, question):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=question,
    )
    return response.text


def compare_strategies(openai_strategy, gemini_strategy):
    if openai_strategy == gemini_strategy:
        print("MATCH:", openai_strategy)
        return True
    else:
        print("MISMATCH:")
        print("OpenAI:", openai_strategy)
        print("Gemini:", gemini_strategy)
        return False


def judge_strategies(openai_strategy, gemini_strategy, openai_data, gemini_data):
    judge_prompt = f"""Two anonymous advisors suggested different options strategies for a complete beginner with a 200 dollar budget who wants to avoid large losses.

Advisor A suggested: {openai_strategy}. Reason: {openai_data["reason"]}
Advisor B suggested: {gemini_strategy}. Reason: {gemini_data["reason"]}

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

    gemini_answer = ask_gemini(gemini_client, question)
    print("Gemini:", gemini_answer)

    try:
        openai_data = json.loads(openai_answer)
        gemini_data = json.loads(gemini_answer)
    except json.JSONDecodeError:
        print("Could not parse one of the responses. Stopping.")
        return
    openai_strategy = openai_data["strategy"]
    gemini_strategy = gemini_data["strategy"]

    is_match = compare_strategies(openai_strategy, gemini_strategy)
    if not is_match:
        judge_strategies(openai_strategy, gemini_strategy, openai_data, gemini_data)


if __name__ == "__main__":
    main()
