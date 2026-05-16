from __future__ import annotations

import pandas as pd


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for strat, g in df.groupby("strategy"):
        lat = pd.to_numeric(g["latency_ms"], errors="coerce").fillna(0)
        succ = g["success"].astype(bool)
        total_tokens = pd.to_numeric(g["total_tokens"], errors="coerce").fillna(0)
        mem = pd.to_numeric(g["memory_pressure_gb"], errors="coerce").fillna(0)
        costs = pd.to_numeric(g["cost_usd"], errors="coerce").fillna(0)

        rows.append(
            {
                "strategy": strat,
                "avg_latency_ms": float(lat.mean()),
                "p95_latency_ms": float(lat.quantile(0.95)),
                "p99_latency_ms": float(lat.quantile(0.99)),
                "throughput_req_per_s": float(len(g) / max(0.001, lat.sum() / 1000.0)),
                "gpu_memory_util_avg_gb": float(mem.mean()),
                "rejection_rate": float((~succ).mean()),
                "cost_per_1000_req_usd": float(costs.sum() / max(1, len(g)) * 1000),
                "tokens_per_sec": float(total_tokens.sum() / max(0.001, lat.sum() / 1000.0)),
            }
        )
    return pd.DataFrame(rows).sort_values("strategy")
