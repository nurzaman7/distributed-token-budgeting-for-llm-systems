#!/usr/bin/env python3
from __future__ import annotations

import pandas as pd
from observability.metrics import summarize
from observability.store import read_results


def main() -> int:
    df = read_results()
    out = summarize(df)
    print(out.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
