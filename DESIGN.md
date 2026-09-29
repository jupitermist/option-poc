# Architecture Decision Records

### ADR-001: Two advisors plus a neutral judge
**Status:** Accepted
**Context:** Trusting a single AI for a financial decision is fragile — one model's
bias or error goes unchecked.
**Decision:** Two models (OpenAI, Gemini) propose independently. A third model
(Claude) judges only when they disagree.
**Consequences:** Cross-checking catches single-model errors and surfaces trade-offs.
Costs more API calls and latency than asking one model.

### ADR-002: The judge is not one of the advisors
**Status:** Accepted
**Context:** If a judging model had also proposed one of the answers, it could favor
its own suggestion.
**Decision:** Claude judges but never proposes. The two suggestions are anonymized
("Advisor A / B") so the judge cannot tell which model said what.
**Consequences:** Removes the advisor's stake in the verdict. Requires a third
provider and key.

### ADR-003: Fixed judging criteria
**Status:** Accepted
**Context:** "Which is better?" is subjective and produces inconsistent verdicts.
**Decision:** The judge scores only on three explicit criteria: cost to enter, risk
of large loss, and beginner-friendliness.
**Consequences:** Verdicts are consistent and explainable. Ignores factors outside
the three criteria.

### ADR-004: Constrain output to five named strategies as JSON
**Status:** Accepted
**Context:** Free-text answers can't be compared reliably — the same strategy gets
worded differently, breaking equality checks.
**Decision:** Limit strategies to five named options and require JSON output.
**Consequences:** The two answers can be compared programmatically. Excludes
strategies outside the five.

### ADR-005: Ground suggestions in real market data
**Status:** Accepted
**Context:** Without real data, the tool is just a chatbot — the suggestion doesn't
respond to the actual stock.
**Decision:** Fetch recent price and trend via yfinance, and instruct the models to
choose based on the trend.
**Consequences:** Suggestions vary by stock and market state. Adds a data dependency
and a slower run.

### ADR-006: A separate evaluation script, not a feature
**Status:** Accepted
**Context:** I wanted to measure how reliable the advisors are, without mixing that
into the advice flow.
**Decision:** `evaluate.py` runs the advisors N times and reports their agreement
rate, reusing the advisor's own functions.
**Consequences:** Keeps advice and measurement separate. It surfaced a finding: the
two models often disagree, and each model's variability differs — evidence that one
model alone is not enough.