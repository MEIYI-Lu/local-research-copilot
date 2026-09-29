from __future__ import annotations

import re
from dataclasses import dataclass


SUSPICIOUS_PATTERNS = [
    r"ignore (all|any|the|your)?\s*(previous|prior) instructions",
    r"reveal (the )?(system|developer) prompt",
    r"show (me )?(the )?(system|developer) prompt",
    r"you are now",
    r"override (the )?(rules|instructions)",
    r"do not follow (the )?(system|developer) instructions",
]


@dataclass(frozen=True)
class GuardResult:
    safe: bool
    reason: str = ""


def inspect_text(text: str) -> GuardResult:
    lowered = text.lower()
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, lowered):
            return GuardResult(False, f"Matched suspicious instruction pattern: {pattern}")
    return GuardResult(True)


def filter_untrusted_chunks(chunks: list[str]) -> tuple[list[str], int]:
    clean: list[str] = []
    removed = 0
    for text in chunks:
        if inspect_text(text).safe:
            clean.append(text)
        else:
            removed += 1
    return clean, removed
