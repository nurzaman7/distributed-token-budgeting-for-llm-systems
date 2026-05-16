from __future__ import annotations

from fastapi import FastAPI
import pandas as pd

from simulator.engine import simulate_all
from observability.store import init_db, read_results, write_results
from observability.metrics import summarize

app = FastAPI(title="Distributed Token Budgeting Lab", version="0.1.0")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "distributed-token-budgeting-lab"}


@app.post("/simulate")
def simulate(requests: int = 10000, seed: int = 42) -> dict:
    rows = simulate_all(n=requests, seed=seed)
    df = pd.DataFrame(rows)
    write_results(df)
    return {"rows_written": len(df), "strategies": int(df["strategy"].nunique())}


@app.get("/results")
def results(limit: int = 200) -> list[dict]:
    df = read_results()
    return df.tail(max(1, min(limit, 10000))).to_dict(orient="records")


@app.get("/metrics")
def metrics() -> list[dict]:
    df = read_results()
    return summarize(df).to_dict(orient="records")
