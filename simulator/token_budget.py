from __future__ import annotations


def compress_prompt_tokens(prompt_tokens: int, priority: int) -> int:
    # low-priority requests get aggressive compression.
    if priority == 1:
        return int(prompt_tokens * 0.55)
    if priority == 2:
        return int(prompt_tokens * 0.70)
    return int(prompt_tokens * 0.82)


def context_window_policy(prompt_tokens: int, max_window: int = 32768) -> tuple[int, int, int]:
    # returns (kept, summarized, dropped)
    if prompt_tokens <= max_window:
        return prompt_tokens, 0, 0
    overflow = prompt_tokens - max_window
    summarized = int(overflow * 0.8)
    dropped = overflow - summarized
    kept = max_window
    return kept, summarized, dropped
