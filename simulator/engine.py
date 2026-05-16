from __future__ import annotations

from simulator.generator import generate_requests
from simulator.strategies import (
    run_compression_first,
    run_naive,
    run_short_long_pool,
    run_token_aware,
)


def simulate_all(n: int = 10_000, seed: int = 42) -> list[dict]:
    reqs = generate_requests(n=n, seed=seed)
    out: list[dict] = []

    for r in reqs:
        out.append(run_naive(r).model_dump())
        out.append(run_token_aware(r).model_dump())
        out.append(run_compression_first(r).model_dump())
        out.append(run_short_long_pool(r).model_dump())

    return out
