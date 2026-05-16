#!/usr/bin/env python3
from __future__ import annotations

import argparse
import pandas as pd

from simulator.engine import simulate_all
from observability.store import init_db, write_results


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--requests", type=int, default=10000)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    rows = simulate_all(n=args.requests, seed=args.seed)
    df = pd.DataFrame(rows)
    init_db()
    write_results(df)
    print(f"wrote {len(df)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
