# distributed-token-budgeting-for-llm-systems

A hands-on lab for understanding how future LLM systems control token usage, latency, memory, and cost across distributed inference infrastructure.

## Why this project exists

Tokens are a distributed-systems resource, not just an NLP concept.

- **Memory**: long prompts increase KV-cache pressure and reduce serving capacity.
- **Latency**: larger token budgets consume more compute and queue time.
- **Cost**: token-heavy traffic drives inference spend.
- **Throughput**: naive routing can let long-context requests bottleneck the cluster.

This lab teaches and simulates how token-aware infrastructure policies improve system behavior.

## What is implemented (MVP)

Core modules:
1. **Token Budget Router** (naive vs token-aware vs compression-first vs short/long-context pools)
2. **Context Window Manager** (keep/summarize/drop policy)
3. **Prompt Compression Engine** (priority-aware compression)
4. **KV Cache Simulator** (token->memory pressure estimation)
5. **Distributed Batching Scheduler** (continuous batching simulation)
6. **Token Observability Dashboard** (latency/throughput/cost/memory/rejection visualizations)
7. **Benchmark Suite** (strategy comparison outputs)

## Repository structure

```text
distributed-token-budgeting-for-llm-systems/
├── README.md
├── docs/
├── examples/
├── benchmarks/
├── simulator/
├── observability/
├── dashboard/
├── tests/
└── notebooks/
```

## Simulation model

For each synthetic request we estimate:
- prompt tokens
- output tokens
- total token budget
- memory pressure
- latency
- cost
- routing pool
- success/failure

Workload size:
- default: **10,000 requests**
- four strategies evaluated per request

## Strategy comparison included

1. `naive`
2. `token_aware`
3. `compression_first`
4. `short_long_pool`

## Metrics provided

- average latency
- P95 latency
- P99 latency
- throughput
- GPU memory utilization (simulated)
- rejection rate
- cost per 1,000 requests
- tokens/sec

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./scripts_run_api.sh
```

In another terminal:

```bash
source .venv/bin/activate
./scripts_run_dashboard.sh
```

- API docs: `http://localhost:8080/docs`
- Dashboard: `http://localhost:8501`

## API endpoints

- `GET /health`
- `POST /simulate?requests=10000&seed=42`
- `GET /results?limit=...`
- `GET /metrics`

## Benchmark

```bash
python benchmarks/run_benchmark.py
```

## Educational outcomes

This project demonstrates:
- why long-context requests create system bottlenecks
- how token-aware routing improves throughput and stability
- how prompt compression and context management reduce load
- how KV-cache pressure links token size to memory and serving capacity
- how observability metrics guide infrastructure decisions
