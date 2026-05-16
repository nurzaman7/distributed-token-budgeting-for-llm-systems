from __future__ import annotations

import numpy as np
from simulator.models import LLMRequest


def generate_requests(n: int = 10_000, seed: int = 42) -> list[LLMRequest]:
    rng = np.random.default_rng(seed)

    prompt = rng.lognormal(mean=6.3, sigma=0.8, size=n).astype(int)
    prompt = np.clip(prompt, 128, 120000)

    output = rng.lognormal(mean=5.5, sigma=0.6, size=n).astype(int)
    output = np.clip(output, 64, 32000)

    priority = rng.choice([1, 2, 3], size=n, p=[0.6, 0.3, 0.1])

    return [
        LLMRequest(
            request_id=i,
            prompt_tokens=int(prompt[i]),
            expected_output_tokens=int(output[i]),
            priority=int(priority[i]),
        )
        for i in range(n)
    ]
