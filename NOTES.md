This PoC started as an option "autopsy" tool and evolved into a strategy advisor.

The original goal was to explain *why* an option's price moved (delta, theta, or
gamma) over a few days, using Black-Scholes values as ground truth. It worked, but
it answered "what happened?" — a question no beginner actually asks. The real
problem I had was the opposite: I wanted to trade options but couldn't decide what
to do first.

So I refocused the PoC on that decision. The harder part turned out not to be
generating a suggestion — any chatbot can do that — but making the suggestion
trustworthy: grounding it in real market data, and not relying on a single AI's
word. I treated "trusting one model" as the core risk, and built the tool around
cross-checking instead. This is a reasonable stopping point for the current scope.