import sys

from advisor import (
    build_question,
    ask_openai,
    ask_gemini,
    get_strategy,
    compare_strategies,
    openai_client,
    gemini_client,
)


def run_agreement_test(ticker, n):
    match_count = 0
    for i in range(n):
        question = build_question(ticker)
        openai_strategy, _ = get_strategy(ask_openai(openai_client, question))
        gemini_strategy, _ = get_strategy(ask_gemini(gemini_client, question))
        print(f"Run {i+1}:")
        if compare_strategies(openai_strategy, gemini_strategy):
            match_count += 1
    print(f"\nAgreement: {match_count} / {n}")


if __name__ == "__main__":
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    run_agreement_test(ticker, 3)
