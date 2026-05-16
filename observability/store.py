from __future__ import annotations

import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = "data/token_budget_lab.db"


def init_db(path: str = DB_PATH) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS results (
                request_id INTEGER,
                strategy TEXT,
                prompt_tokens INTEGER,
                output_tokens INTEGER,
                total_tokens INTEGER,
                memory_pressure_gb REAL,
                latency_ms REAL,
                cost_usd REAL,
                routing_pool TEXT,
                success INTEGER,
                rejected_reason TEXT
            )
            """
        )


def write_results(df: pd.DataFrame, path: str = DB_PATH) -> None:
    with sqlite3.connect(path) as conn:
        df.to_sql("results", conn, if_exists="replace", index=False)


def read_results(path: str = DB_PATH) -> pd.DataFrame:
    with sqlite3.connect(path) as conn:
        return pd.read_sql_query("SELECT * FROM results", conn)
