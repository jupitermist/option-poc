This PoC started as an option "autopsy" tool and evolved into a strategy advisor.

The original goal was to explain *why* an option's price moved (delta, theta, or
gamma) over a few days, using Black-Scholes values as ground truth. It worked, but
it answered "what happened?" — not a question a beginner actually faces. The real
challenge for a beginner is the opposite: wanting to start trading options, but
being unable to decide which strategy to pick first.

So the PoC was refocused on that decision. The hard part is not generating a
suggestion — any chatbot can do that — but making the suggestion trustworthy:
grounding it in real market data, and not relying on a single AI's word. "Trusting
one model" was treated as the core risk, and the tool was designed around
cross-checking instead. This is a reasonable stopping point for the current scope.