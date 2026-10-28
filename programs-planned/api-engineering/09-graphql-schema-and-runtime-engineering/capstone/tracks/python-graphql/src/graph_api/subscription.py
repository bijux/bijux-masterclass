"""Resume validation for an ordered subscription event stream."""

from __future__ import annotations

from dataclasses import dataclass

from .model import ValidationError


@dataclass(frozen=True)
class SubscriptionEvent:
    sequence: int
    payload: dict[str, object]


class ResumableSubscription:
    """Suppress duplicates, reject gaps, and bound buffered delivery."""

    def __init__(self, *, maximum_buffer: int = 100) -> None:
        if maximum_buffer < 1:
            raise ValueError("maximum_buffer must be positive")
        self.maximum_buffer = maximum_buffer

    def resume(
        self,
        events: list[SubscriptionEvent],
        *,
        after: int,
    ) -> list[SubscriptionEvent]:
        ordered = sorted(events, key=lambda event: event.sequence)
        delivered: list[SubscriptionEvent] = []
        expected = after + 1
        seen: set[int] = set()

        for event in ordered:
            if event.sequence <= after or event.sequence in seen:
                continue
            if event.sequence != expected:
                raise ValidationError(
                    "subscription gap: "
                    f"expected {expected}, got {event.sequence}"
                )

            delivered.append(event)
            seen.add(event.sequence)
            expected += 1

            if len(delivered) > self.maximum_buffer:
                raise ValidationError("subscription buffer exceeded")

        return delivered
