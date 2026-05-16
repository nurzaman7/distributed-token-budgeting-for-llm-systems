from __future__ import annotations

from pydantic import BaseModel, Field


class LLMRequest(BaseModel):
    request_id: int
    prompt_tokens: int
    expected_output_tokens: int
    priority: int = Field(ge=1, le=3)


class SimResult(BaseModel):
    request_id: int
    strategy: str
    prompt_tokens: int
    output_tokens: int
    total_tokens: int
    memory_pressure_gb: float
    latency_ms: float
    cost_usd: float
    routing_pool: str
    success: bool
    rejected_reason: str | None = None
