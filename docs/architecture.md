# Architecture

Flow:
1. Synthetic request generator creates diverse token demands.
2. Four routing strategies simulate serving choices.
3. Each request generates memory, latency, cost, and success outcomes.
4. Results are stored in SQLite.
5. Metrics layer computes latency/throughput/cost KPIs.
6. FastAPI serves results and metrics.
7. Streamlit visualizes strategy tradeoffs.
