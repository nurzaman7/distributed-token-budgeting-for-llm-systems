from __future__ import annotations

from simulator.models import LLMRequest, SimResult
from simulator.token_budget import compress_prompt_tokens, context_window_policy

TOKENS_PER_GB = 35000  # rough KV-cache pressure conversion
GPU_CAPACITY_GB = {"small": 24, "medium": 40, "large": 80}
COST_PER_1K_TOKENS = 0.004


def _estimate_memory_gb(total_tokens: int) -> float:
    return total_tokens / TOKENS_PER_GB


def _estimate_latency_ms(total_tokens: int, memory_gb: float, overload_factor: float = 1.0) -> float:
    base = 35 + (total_tokens * 0.012)
    pressure_penalty = max(0.0, memory_gb - 20) * 4.5
    return (base + pressure_penalty) * overload_factor


def _cost_usd(total_tokens: int) -> float:
    return (total_tokens / 1000.0) * COST_PER_1K_TOKENS


def run_naive(req: LLMRequest) -> SimResult:
    total = req.prompt_tokens + req.expected_output_tokens
    mem = _estimate_memory_gb(total)
    pool = "default"
    success = mem <= GPU_CAPACITY_GB["medium"]
    reason = None if success else "oom_or_kv_pressure"
    return SimResult(
        request_id=req.request_id,
        strategy="naive",
        prompt_tokens=req.prompt_tokens,
        output_tokens=req.expected_output_tokens,
        total_tokens=total,
        memory_pressure_gb=round(mem, 3),
        latency_ms=round(_estimate_latency_ms(total, mem, overload_factor=1.2), 3),
        cost_usd=round(_cost_usd(total), 6),
        routing_pool=pool,
        success=success,
        rejected_reason=reason,
    )


def run_token_aware(req: LLMRequest) -> SimResult:
    total = req.prompt_tokens + req.expected_output_tokens
    mem = _estimate_memory_gb(total)

    if total < 12000:
        pool = "small"
    elif total < 48000:
        pool = "medium"
    else:
        pool = "large"

    success = mem <= GPU_CAPACITY_GB[pool]
    reason = None if success else "pool_capacity_exceeded"

    overload = 0.95 if pool == "large" else 1.0
    return SimResult(
        request_id=req.request_id,
        strategy="token_aware",
        prompt_tokens=req.prompt_tokens,
        output_tokens=req.expected_output_tokens,
        total_tokens=total,
        memory_pressure_gb=round(mem, 3),
        latency_ms=round(_estimate_latency_ms(total, mem, overload), 3),
        cost_usd=round(_cost_usd(total), 6),
        routing_pool=pool,
        success=success,
        rejected_reason=reason,
    )


def run_compression_first(req: LLMRequest) -> SimResult:
    compressed_prompt = compress_prompt_tokens(req.prompt_tokens, req.priority)
    total = compressed_prompt + req.expected_output_tokens
    mem = _estimate_memory_gb(total)

    pool = "medium" if total < 52000 else "large"
    success = mem <= GPU_CAPACITY_GB[pool]
    reason = None if success else "capacity_after_compression_exceeded"

    return SimResult(
        request_id=req.request_id,
        strategy="compression_first",
        prompt_tokens=compressed_prompt,
        output_tokens=req.expected_output_tokens,
        total_tokens=total,
        memory_pressure_gb=round(mem, 3),
        latency_ms=round(_estimate_latency_ms(total, mem, 0.92), 3),
        cost_usd=round(_cost_usd(total), 6),
        routing_pool=pool,
        success=success,
        rejected_reason=reason,
    )


def run_short_long_pool(req: LLMRequest) -> SimResult:
    kept, summarized, _ = context_window_policy(req.prompt_tokens, max_window=32768)
    eff_prompt = kept + int(summarized * 0.25)
    total = eff_prompt + req.expected_output_tokens
    mem = _estimate_memory_gb(total)

    pool = "short_ctx" if req.prompt_tokens <= 32768 else "long_ctx"
    cap = 30 if pool == "short_ctx" else 80
    success = mem <= cap
    reason = None if success else "context_pool_oom"

    overload = 0.9 if pool == "long_ctx" else 1.05
    return SimResult(
        request_id=req.request_id,
        strategy="short_long_pool",
        prompt_tokens=eff_prompt,
        output_tokens=req.expected_output_tokens,
        total_tokens=total,
        memory_pressure_gb=round(mem, 3),
        latency_ms=round(_estimate_latency_ms(total, mem, overload), 3),
        cost_usd=round(_cost_usd(total), 6),
        routing_pool=pool,
        success=success,
        rejected_reason=reason,
    )
