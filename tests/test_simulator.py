import pandas as pd

from simulator.engine import simulate_all
from observability.metrics import summarize


def test_simulator_row_count():
    rows = simulate_all(n=100, seed=1)
    assert len(rows) == 400


def test_metrics_contains_strategies():
    rows = simulate_all(n=100, seed=2)
    df = pd.DataFrame(rows)
    out = summarize(df)
    assert set(out["strategy"].tolist()) == {"naive", "token_aware", "compression_first", "short_long_pool"}
